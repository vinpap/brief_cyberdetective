import pandas as pd
from scrapers import Books_scraper, Selenium_scraper

"""
Utilisez Books_scraper pour scraper le site books.toscrape.com avec
BeautifulSoup uniquement, et Selenium_scraper pour scraper le site avec 
Selenium
"""

scraper = Books_scraper()
#scraper = Selenium_scraper()
df = scraper.scrape(pages_count=100)
df.to_csv("books_info.csv", sep="|")




