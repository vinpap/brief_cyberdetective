# brief_cyberdetective

Voici le repository pour le brief n°14 : cyber-détective. Il comprend les fichiers suivants :
- get_books_info.py : extrait les informations concernant les livres présentés sur le site books.toscrape.com
- books.sql : le code SQL qui permet de créer la base de données qui contient les données précédemment extraites
- all_books_analysis.py : un fichier qui analyse ces données.

Les fichiers suivants ont trait au scraping de Twitter :
- twitter_scraper.py : ce script est issu de l'un de mes anciens projets. Il contient une classe qui scrape automatiquement Twitter à l'aide de la librairie snscrape.
- twitter_scraping_script.py : contient seulement quelques lignes qui appellent les fonctions de la classe Scraper définie dans twitter_scraper.py
