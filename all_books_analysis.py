import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("Analyse des données collectées sur books.toscrape.com")
books_df = pd.read_csv("books_info.csv", sep="|")
print(books_df.info())

print("Analyse des différentes colonnes :")
#sns.boxplot(books_df["uk price"])
sns.histplot(books_df["uk price"]).set(title="Répartition des prix des livres")
plt.show()

sns.histplot(books_df["rating"]).set(title="Répartition des notes des livres")
plt.show()

sns.countplot(x=books_df["availability"]).set(title="Répartition des statuts de disponibilité")
plt.show()

print("Conclusions :")
print("- Les prix des livres sont répartis équitablement entre 0 et 60 £")
print("- De la même manière, les notes des livres sont elles aussi réparties aléatoirement")
print("- Tous les articles sont disponibles.\n")
print("""En ce qui concerne les deux premiers points, on notera qu'il n'y a rien d'étonnant à 
constater ces phénomènes dans la mesure où les données numériques utilisées sur ce site ont été générées aléatoirement.""")