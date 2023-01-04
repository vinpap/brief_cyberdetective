import time
from scrapers import Twitter_scraper

"""
Ce script utilise la classe Twitter_scraper pour extraire automatiquement des tweets en fonction
des paramètres donnés
"""

test = Twitter_scraper(format="csv")
t1 = int(time.time())
test.scrape(query="the art of war", language="en", results_count=5000, filepath="data/en/the_art_of_war.csv")
t2 = int(time.time())
print("Process finished in " + str(t2-t1) + " seconds")