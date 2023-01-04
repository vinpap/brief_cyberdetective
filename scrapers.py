import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from snscrape.modules.twitter import TwitterSearchScraper

class Books_scraper:

	"""
	Scrape le site books.toscrape.com à l'aide de BeautifulSoup.
	Pour une approche à l'aide de Selenium, cf Selenium_scraper
	"""

	def __init__(self): 

		self.url = "https://books.toscrape.com/catalogue/"

	def scrape(self, pages_count=10):
		"""
		pages_count is the number of pages we want to scrape.
		If set higher than the total number of pages, it scraps
		from all available pages.
		Returns a dataframe containing the data that was extracted.
		"""

		# This dataframe will store all the book details
		books_df = pd.DataFrame()

		for i in range(1, pages_count+1):

			response = requests.get(self.url + "page-" + str(i) + ".html")

			# If the response code is 400 or more, it means we reached
			# the end of the catalogue, so we stop parsing
			if not response.ok: break

			page_df = self.scrape_page(response.text)
			books_df = pd.concat([books_df, page_df])
			print(f"{i} catalogue pages processed")

		clean_df = self.clean_dataframe(books_df)
		clean_df.reset_index(inplace=True)
		clean_df.drop(columns=["index"], inplace=True)
		return clean_df


	def get_book_details(self, soup):
		"""Takes the HTML code for a single book's details
		and returns a dictionary with all the info we are 
		looking for about the book"""

		# The dictionary that will contain the book's details
		book_details = {}

		book_details["title"] = soup.find_all("a")[-1]["title"]
		book_details["uk price"] = soup.find("p", {"class": "price_color"}).text

		if soup.find("p", {"class": "star-rating One"}) : 
			book_details["rating"] = 1
		elif soup.find("p", {"class": "star-rating Two"}) : 
			book_details["rating"] = 2
		elif soup.find("p", {"class": "star-rating Three"}) : 
			book_details["rating"] = 3
		elif soup.find("p", {"class": "star-rating Four"}) : 
			book_details["rating"] = 4
		elif soup.find("p", {"class": "star-rating Five"}) : 
			book_details["rating"] = 5

		book_details["availability"] = soup.find("p", {"class": "instock availability"}).text.strip()
		book_details["image url"] = soup.find("img")["src"]

		return book_details

	def scrape_page(self, html):
		"""Scrapes a whole result page and returns a DataFrame
		where each line contains all the information regarding 
		a book"""

		soup = BeautifulSoup(html, "lxml")
		# A list of dictionaries that contains all books' information
		books = []

		for book in soup.find_all("article", {"class": "product_pod"}):
			book_info = self.get_book_details(book)
			books.append(book_info)

		return pd.DataFrame(books)

	def clean_dataframe(self, df):
		"""Some columns in the dataframe need to be formatted. The values 
		in the price column contain an extra 'Â' at the beginning of
		each value, and the image url is a relative link. This function
		takes care of these issues"""

		print("Data before cleaning:")
		print(df.info())
		print(df.head())

		# We remove the extra 'A' at the beginning of the prices. Moreover,
		# we remove the currency symbols as all prices are in UK pounds
		df["uk price"] = df["uk price"].str[2:]

		# As for the image url column, we replace the .. at the beginning
		# of each link by the full internet address
		df["image url"] = df["image url"].str[2:]
		df["image url"] = "https://books.toscrape.com" + df["image url"]

		print("Data after cleaning:")
		print(df.info())
		print(df.head())

		return df

class Selenium_scraper(Books_scraper):
	"""
	Cette classe scrape le site books.toscrape.com à l'aide de Selenium.
	"""

	def __init__(self):

		self.url = "https://books.toscrape.com"
		service = ChromeService(executable_path=ChromeDriverManager().install())
		self.driver = webdriver.Chrome(service=service)
		self.driver.set_window_size(1920, 1080)

	def scrape(self, pages_count=10):
		"""
		pages_count is the number of pages we want to scrape.
		If set higher than the total number of pages, it scraps
		from all available pages.
		Returns a dataframe containing the data that was extracted.
		"""

		# This dataframe will store all the book details
		books_df = pd.DataFrame()
		self.driver.get(self.url)

		keep_scraping = True
		scraped_pages = 0
		while keep_scraping:

			page_df = self.scrape_page(self.driver.page_source)
			books_df = pd.concat([books_df, page_df])
			
			scraped_pages += 1
			if scraped_pages >= pages_count:
				keep_scraping = False
			print(f"{scraped_pages} catalogue pages processed")

			try:
				btn = self.driver.find_element(By.CSS_SELECTOR, '#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next > a')
				btn.click()

			except NoSuchElementException:
				keep_scraping=False

		self.driver.quit()
		clean_df = self.clean_dataframe(books_df)
		clean_df.reset_index(inplace=True)
		clean_df.drop(columns=["index"], inplace=True)
		return clean_df



class Twitter_scraper:

	"""
	©Vincent

	Cette classe fait initialement partie d'un projet développé il y a 1-2 ans, elle permet de scraper 
	automatiquement les tweets à partir des paramètres que vous lui communiquez.
	Exemple d'utilisation (code dans un fichier séparé) :

	from twitter_scraper import Twitter_scraper

	test = Twitter_scraper(format="csv")
	test.scrape(query="Votre recherche", language="fr", results_count=500, filepath="results.csv")

	Lisez la doc de chaque fonction pour comprendre à quoi sert chaque paramètre, et demandez-moi 
	si vous avez des questions
	"""

	def __init__(self, format=""):
		"""
		À l'origine le scraper devait aussi gérer le JSON, d'où le paramètre format.
		Valeurs possibles : 
		- "csv" pour enregistrer les résultats dans un csv
		- n'importe quelle autre valeur si vous voulez juste afficher les résultats dans la console
		"""
		
		self.supported_formats = ["csv"]
		if format in self.supported_formats:
			self.format = format
			self.display_only = False
		else:
			print(f"WARNING: format {format} is not supported. Switching to display only")
			self.display_only = True
			return



	def scrape(self, filepath=None, query=None, results_count=0, language="en"):

		"""
		Paramètres :
		- filepath : chemin vers le fichier où vous voulez enregistrer vos données
		- query : la recherche que vous voulez effectuer
		- results_count : le nombre de résultats voulus
		- language : la langue de recherche ("en" pour anglais, "fr" pour français)
		"""

		tweets_max_time = int(time.time()) - 604800

		search = query + " lang:" + language + " since:2022-06-01"
		required_fields = ["id", "url", "date", "renderedContent", "hashtags", "replyCount", "retweetCount", "likeCount"]

		scraped_data = []
		tweets_processed = 0
		chunk_size = 10000

		while tweets_processed < results_count:
			scraping_results = TwitterSearchScraper(search).get_items()
			while tweets_processed < results_count:
				try:
					tweet = next(scraping_results)
					tweet.renderedContent = '''%s''' % tweet.renderedContent
					if tweet.hashtags:
						tweet.hashtags = str(tweet.hashtags).lstrip('[').rstrip(']')
						tweet.hashtags = '''%s''' % tweet.hashtags

				except (TypeError, KeyError):
					continue
				except StopIteration:
					tweets_max_time -= 3000
					search = query + " lang:" + language + " until_time:" + str(tweets_max_time)
					break
				tweets_processed+=1
				if tweets_processed % 100 == 0:
					print(str(tweets_processed) + " tweets scraped")
				scraped_data.append(tweet)
				if tweets_processed % chunk_size == 0:
					print("Saving data chunk")
					scraped_data = pd.DataFrame(scraped_data)[required_fields]
					self.output(scraped_data)
					scraped_data = []

		print("Final save")
		if scraped_data != []:
			scraped_data = pd.DataFrame(scraped_data)[required_fields]
			self.output(scraped_data, filepath)

	def output(self, scraped_data, filepath):

		"""Ici, on enregistre ou affiche les résultats"""
		if self.display_only:
			print(scraped_data)

		elif self.format == "csv":
			scraped_data.to_csv(filepath, index=False, sep ='|')


