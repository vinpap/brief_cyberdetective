import string
import pandas as pd
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import RegexpTokenizer
from wordcloud import WordCloud, STOPWORDS

"""Le code ci-dessous affiche les nuages de mots correspondant aux données
passées en paramètre à la fonction make-tag_cloud
"""

# On télécharge les ressources nécessaires à NLTK et on initialise notre
# tokenizer
nltk.download("stopwords")
nltk.download("punkt")
tokenizer = RegexpTokenizer(r'\w+')


def make_tag_cloud(filepath, stopwords=[]):
	"""
	filepath : chemin vers le fichier csv qui contient les tweets à analyser
	stopwords : stopwords additionnels qui peuvent être définis par l'utilisateur
	(mots à ignorer dans le nuage de mots)
	"""

	# En plus des mots passés en paramètre, on ignore tous les mots composés d'une seule lettre et les
	# mots simples de l'anglais contenus dans les stopwords de NLTK
	stopwords.extend(["http", "https"])
	custom_stopwords = stopwords
	stop_words = nltk.corpus.stopwords.words('english')
	stop_words = set(stop_words + list(STOPWORDS) + custom_stopwords + list(string.ascii_lowercase))

	# Tokenization de tout notre texte
	tweets = pd.read_csv(filepath, sep="|")["renderedContent"]
	tweets = tweets.str.lower()
	tweets = tweets.apply(lambda row: tokenizer.tokenize(row))
	tweets = tweets.sum()
	tweets = " ".join(tweets)

	wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words,
                collocations=False,
                min_font_size = 10).generate(tweets)
                     
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)
	 
	plt.show()


# Enlever les commentaires sur les lignes ci-dessous, en fonction des nuages de mots que l'on
# souhaite afficher. On passe en stopwords les titres des livres, qui ne sont pas pertinents
# et prennent beaucoup de place dans les nuages.

#make_tag_cloud("data/en/the_art_of_war.csv", stopwords=["war", "art"])
#make_tag_cloud("data/en/the_song_of_achille.csv", stopwords=["song", "achille", "achilles"])
#make_tag_cloud("data/en/batman_the_dark_night_return.csv", stopwords=["batman", "dark", "knight", "return"])
#make_tag_cloud("data/en/the_picture_of_dorian_gray.csv", stopwords=["picture", "dorian", "gray"])
#make_tag_cloud("data/en/the_book_thief.csv", stopwords=["book", "thief"])

