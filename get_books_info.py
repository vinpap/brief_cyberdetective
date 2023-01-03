import requests
import pandas as pd
from bs4 import BeautifulSoup

# The base URL to scrape at
url = "https://books.toscrape.com/catalogue/"

# The number of pages we want to scrape on the website
# If this value is higher than the number of pages, it will
# scrape everything
pages_to_scrape = 100


def get_book_details(soup):
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

def scrape_page(html):
	"""Scrapes a whole result page and returns a DataFrame
	where each line contains all the information regarding 
	a book"""

	soup = BeautifulSoup(html, "lxml")
	# A list of dictionaries that contains all books' information
	books = []

	for book in soup.find_all("article", {"class": "product_pod"}):
		book_info = get_book_details(book)
		books.append(book_info)

	return pd.DataFrame(books)

def clean_dataframe(df):
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


# This dataframe will store all the book details
books_df = pd.DataFrame()

for i in range(1, pages_to_scrape+1):

	response = requests.get(url + "page-" + str(i) + ".html")

	# If the response code is 400 or more, it means we reached
	# the end of the catalogue, so we stop parsing
	if not response.ok: break

	page_df = scrape_page(response.text)
	books_df = pd.concat([books_df, page_df])
	print(f"{i} catalogue pages processed")

clean_df = clean_dataframe(books_df)
clean_df.reset_index(inplace=True)
clean_df.drop(columns=["index"], inplace=True)
clean_df.to_csv("books_info.csv", sep="|")




