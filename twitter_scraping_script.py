import time
from twitter_scraper import Scraper

test = Scraper(format="csv")
t1 = int(time.time())
test.scrape(query="%23The Art of War", language="en", results_count=100, filepath="the_art_of_war.csv")
t2 = int(time.time())
print("Process finished in " + str(t2-t1) + " seconds")