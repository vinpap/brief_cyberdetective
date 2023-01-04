# brief_cyberdetective

Voici le repository pour le brief n°14 : cyber-détective. Il comprend les fichiers suivants :
- get_books_info.py : extrait les informations concernant les livres présentés sur le site books.toscrape.com en utilisant les scrapers codés dans scrapers.py
- books.sql : le code SQL qui permet de créer la base de données qui contient les données précédemment extraites
- all_books_analysis.py : un fichier qui analyse ces données.
- scrapers.py : ce fichier contient tous les scrapers utilisés, pour Twitter et pour books.toscrape.com.
- twitter_scraping_script.py : contient seulement quelques lignes qui appellent les fonctions de la classe Twitter_scraper définie dans twitter_scraper.py
- analyse_tweets.ipynb : ce notebook réalise les nuages de mots et les bigrammes/trigrammes à l'aide des tweets. Il réalise aussi des analyses de sentiment
