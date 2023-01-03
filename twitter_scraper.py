"""
©Vincent

Ce module fait initialement partie d'un projet développé il y a 1-2 ans, il permet de scraper 
automatiquement les tweets à partir des paramètres que vous lui communiquez.
Exemple d'utilisation (code dans un fichier séparé) :

from twitter_scraper import Scraper

test = Scraper(format="csv")
test.scrape(query="Votre recherche", language="fr", results_count=500, filepath="results.csv")

Lisez la doc de chaque fonction pour comprendre à quoi sert chaque paramètre, et demandez-moi 
si vous avez des questions
"""


import time
import pandas as pd
from snscrape.modules.twitter import TwitterSearchScraper

class Scraper:

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

