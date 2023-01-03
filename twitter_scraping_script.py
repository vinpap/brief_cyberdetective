import time
from twitter_scraper import Scraper

test = Scraper(format="csv")
t1 = int(time.time())
test.scrape(query="The Art of War", language="en", results_count=5000, filepath="data/en/the_art_of_war.csv")
test.scrape(query="The song of Achille", language="en", results_count=5000, filepath="data/en/the_song_of_achille.csv")
test.scrape(query="Batman : the Dark Night Return", language="en", results_count=5000, filepath="data/en/batman_the_dark_night_return.csv")
test.scrape(query="The Picture of Dorian Gray", language="en", results_count=5000, filepath="data/en/the_picture_of_dorian_gray.csv")
test.scrape(query="The Book Thief", language="en", results_count=5000, filepath="data/en/the_book_thief.csv")
t2 = int(time.time())
print("Process finished in " + str(t2-t1) + " seconds")