import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_book_details(html):
	"""Take the HTML code for a single book's details
	and returns a dictionary with all the info we are 
	looking for about the book"""
	return

def scrape_page(html):
	"""Scrapes a whole result page and returns a DataFrame
	where each line contains all the information regarding 
	a book"""

	soup = BeautifulSoup(html)

	for book in soup.find_all("article", {"class": "product_pod"}):
		pass
	return True

# The base URL to scrape at
url = "https://books.toscrape.com/catalogue/"

# The number of pages we want to scrape on the website
# If this value is higher than the number of pages, it will
# scrape everything
pages_to_scrape = 100

for i in range(1, pages_to_scrape+1):

	response = requests.get(url + "page-" + str(i) + ".html")

	# If the response code is 400 or more, it means we reached
	# the end of the catalogue, so we stop parsing
	if not response.ok: break

	page_df = scrape_page(response.text)
	print(f"{i} catalogue pages processed")

