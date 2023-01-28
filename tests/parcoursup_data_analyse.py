# -*- coding: utf-8 -*-
"""PARCOURSUP_DATA_ANALYSE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CaLyq1azazLa3682fGXkIn8g3O-qlqdO

# **Préambule 📜** 

>Je suis Erwan Coubret, actuellement élève de MP2I qui aime bien jouer avec les données. Alors j'ai récupéré celles de parcoursup et j'ai fait ce notebook pour permettre à tout le monde d'y jeter un coup d'œil facilement. Normalement j'ai fait en sorte que ce qui est mis est compréhensible et facilement modifiable pour qui le veut, à condition d'avoir 2/3 connaissances en python.
> <br/><br/>
> Voilà, pas de soucis de copyright, faites en ce que vous voulez. Si vous avez un problème, vous pouvez me contacter sur twitter : https://twitter.com/ErwanCoubret.

****

## **Pas de prérequis 😊**
>Vous êtes sur un notebook Colaboratory, une adaptation de Jupyter à la sauce Google pour les connaisseurs. Il s'agit d'un service très pratique, utilisant les serveurs de Google pour faire tourner vos scripts (pas mal si vous avez une petite machine où êtes en déplacement). Si jamais vous galérez vraiment allez voir le [tutoriel d'introduction à Colaboratory](https://colab.research.google.com/notebooks/intro.ipynb#scrollTo=GJBs_flRovLc).

**Normalement la base de données est téléchargée automatiquement.** Mais si jamais il y a un problème, voici la procédure  :

**1.**   Rendez vous sur cette URL : https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup/export/ et téléchargez le .csv (cela peut aussi servir si vous voulez jouer avec les données de votre côté)<br/>
**2.**   Cliquez ensuite sur l'icone fichier sur la barre de gauche et importez le .csv, soit en le glissant dans la zone, ou manuellement<br/>
**3.**   Et voilà c'est fini. **(Par contre attention il faudra le remettre si jamais vous quittez la page)**
****

## **Librairies utilisées 📚**

* **🐼 Pandas** : Librairie pour transformer vos datasets en "dataframe", un outil puissant pour manipuler des données.

* **📊 Plotly** : Librairie pour visualiser les données, de manière plus propre que matplotlib, avec notamment une meilleure interaction avec le graphe... Bien qu'encore trop peu utilisée aujourd'hui, la techno est très puissante. Si vous voulez jeter un coup d'oeil aux capacités je vous redirige vers ce tutoriel : https://github.com/antonin-lfv/Plotly_tutorial. Ici on utilisera **plotly.graph_objects**, mais d'autres versions existent, avec leurs propres avantages.


****

# **À l'attaque ⚔️ Récupération des données 📈**

Import des librairies
"""

import pandas as pd
import plotly.graph_objects as go

"""Import de la base de donnée (ça peut prendre un peu de temps)"""

url = "https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-parcoursup/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B" # Lien du dataset

df = pd.read_csv(url, sep=";") # les séparateurs peuvent être différents selon les fichiers .csv, mais ici il y a des ',' dans les titres des colonnes, alors il faut bien préciser qu'on sépare les colonnes grâce aux ';'
print(f"Formations : {df.shape[0]}, Labels de classification : {df.shape[1]}") # Rapide visualisation de la taille du dataset importé

"""Nettoyage des données pour ne garder que celles qui nous intéressent (ici la filière)"""

filière = "CPGE - MP2I" # Ici la filière qu'on veut récupérer pour la traiter, ça marche avec tout autre type de formations présentes dans la colonne "LIB_FOR_VOE_INS" du csv

df = df[df["LIB_FOR_VOE_INS"] == filière] # Ici on récupère uniquement les lignes correspondantes à la formation
print(f"Formations de {filière} référencées : {df.shape[0]}") # Taille du nouveau dataframe avec que la filière choisie
df.head() # Permet d'afficher les 5 premières lignes d'un dataframe, pour avoir une vérification de ce que l'on manipule

"""# **Visualisation 👀**

**Liste des Labels**

Premièrement, observons quels sont les différents moyens de classification avec leur index. Notons que leur index servira prochainement.
"""

for i in range(df.shape[1]):
  print(f"{i} : {df.columns[i]}")

"""**Localisation des formations 🌍**

Attention, certaines formations n'apparaissent pas, de par l'absence de leurs coordonnées GPS
"""

GPSdf = df.dropna(subset=[df.columns[15]]) # On récupère la colonne donnant accès aux coordonnées GPS en éliminant les formations qui ne la renseigne pas

ListLat = []
ListLong = []

for coordonnées in GPSdf[df.columns[15]] : # Les coordonnées référencées sont du type "LAT,LONG" donc on sépare tout ça et on le met dans des listes
    sep = coordonnées.find(',')
    ListLat.append(coordonnées[:sep])
    ListLong.append(coordonnées[sep+1:])

fig = go.Figure()

fig.add_scattermapbox( 
    lon = ListLong,
    lat = ListLat,
    text = GPSdf["Établissement"],
    marker = {'size': 15,
              'color': '#5582ff',
              'opacity' : .7
})

fig.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':10}, # marge left, top, bottom, right
    mapbox = {
        'center': {'lon': 3, 'lat': 47},
        'style': "open-street-map",
        'zoom': 4.5})
        
fig.show()

"""## **Quelques exemples**

> La partie la plus intéressante : voir les données en action. On utilise ici **plotly**, pour les raisons présentées plus tôt. Cependant je me permets de détailler un peu l'interaction avec la figure (le graphe) :

* **Vous pouvez sélectionner les axes que vous souhaitez afficher** en cliquant sur le nom des axes dans la légende. Pour en isoler un en particulier, double-cliquez dessus. Pour tout réafficher, double-cliquez de nouveau et hop. 
* Ensuite, directement sur le graphe, **vous pouvez sélectionner à la souris directement la zone à afficher**
* Et **pour enregistrer**, vous avez en haut à droite un petit menu avec tout à gauche un appareil photo. Un clic et vous pouvez enregistrer

### **Graphes généraux à la filière**
"""

colonnes_à_afficher = [17,44] # Colonnes relatives aux effectifs des cadidats ayant demandé la filière (17) et ceux qui ont reçus une proposition de l'établissement (44)

labels = [df.columns[i] for i in colonnes_à_afficher] # On récupère la liste des labels pour la légende
values = [df[df.columns[i]].mean(axis = 0) for i in colonnes_à_afficher] # On fait la moyenne pour toute la formation

values[0] = values[0] - values[1] # Pour éliminer les candidats déjà comptabilisés

fig = go.Figure(data=[go.Pie(labels=labels, 
                             values=values,
                             hole=.4
)])

fig.update_layout(title=f"% de candidats ayant reçu une proposition d'admission en {filière}") # Titre de la figure

fig.show()

colonnes_à_afficher = [44,45] # Colonnes relatives aux effectifs des candidats ayant reçu une proposition d'admission (44) et ceux ayant accepté celle-ci (45)

labels = [df.columns[i] for i in colonnes_à_afficher]
values = [df[df.columns[i]].mean(axis = 0) for i in colonnes_à_afficher]

values[0] = values[0] - values[1] # Pour éliminer les candidats déjà comptabilisés

fig = go.Figure(data=[go.Pie(labels=labels, 
                             values=values,
                             hole=.4
)])

fig.update_layout(title=f"% des gens acceptant la proposition d'admission de l'établissement en {filière}")

fig.show()

colonnes_à_afficher = [81,82,83,84,85,86] # Colonnes relatives au pourcentage des mentions

labels = [df.columns[i] for i in colonnes_à_afficher]
values = [df[df.columns[i]].mean(axis = 0) for i in colonnes_à_afficher]

fig = go.Figure(data=[go.Pie(labels=labels, 
                             values=values,
                             hole=.4
)])

fig.update_layout(title=f"% correspondant aux mentions obtenues au bac par les admis en {filière}")

fig.show()

colonnes_à_afficher = [17,18] # Colonnes relatives aux effectifs totaux des candidats (17) et des candidates (18)

labels = [df.columns[i] for i in colonnes_à_afficher]
values = [df[df.columns[i]].mean(axis = 0) for i in colonnes_à_afficher]

values[0] = values[0] - values[1]

fig = go.Figure(data=[go.Pie(labels=labels, 
                             values=values,
                             hole=.4
)])

fig.update_layout(title=f"Proportion des candidats/candidates en {filière}")

fig.show()

colonnes_à_afficher = [45,46] # Colonnes relatives au pourcentage des mentions

labels = [df.columns[i] for i in colonnes_à_afficher]
values = [df[df.columns[i]].mean(axis = 0) for i in colonnes_à_afficher]

values[0] = values[0] - values[1]

fig = go.Figure(data=[go.Pie(labels=labels, 
                             values=values,
                             hole=.4
)])

fig.update_layout(title=f"Proportion des admis/admises ayant accepté la proposition de l'établissement {filière}")

fig.show()

"""**NB pour la MP2I (mais peut sûrement s'étendre aux autres filières) :** on observe ici une légère différence entre le rapport des effectifs calculés, et le % reporté ligne 75 vis-à-vis du pourcentage d'admises (affiché dans la cellule suivante : 11,83% d'admises contre 11,4% plus haut). Il faut donc se questionner un peu sur les données, et lui accorder une certaine incertitude, peut-être due à des désistements, des erreurs administratives... """

df[df.columns[75]].mean(axis = 0)

"""### **Graphes particuliers aux établissements**"""

colonne_à_afficher = [17, 20] # On met ici les index des données que l'on souhaite afficher dans la liste, ici le nombre de demandes sans/avec internat correspondent aux index 17 et 20

fig = go.Figure() # Création de la figure avec plotly

for i in colonne_à_afficher:
  fig.add_trace( # Ajout d'un nouvel axe
      go.Bar( # Ici Bar pour créer un histogramme 
          x = df["Établissement"], # on affiche selon le lycée en abscisse
          y = df[df.columns[i]], # et la colonne choisie précédemment dans colonne_à_afficher
          name = df.columns[i] # Nom pour la légende
      )
)

fig.update_layout(title="Nombre de demandes totales/dont internat", # Titre pour la figure
                  xaxis={'categoryorder':'max descending'}) # Permet de trier de manière décroissante selon la valeur maximale de l'axe

fig.show()

colonne_à_afficher = [17, 101] # Index correspondant aux effectifs (17) et le rang du dernier appelé (101)

fig = go.Figure()

for i in colonne_à_afficher:
  fig.add_trace(
      go.Bar(
          x = df["Établissement"],
          y = df[df.columns[i]],
          name = df.columns[i]
      )
)

fig.update_layout(title="Comparatif entre le nombre de demandes et le rang du dernier appelé",
                  xaxis={'categoryorder':'max descending'}
)

fig.show()

colonne_à_afficher = 75 # Ligne correspondant à la proportion de filles par formations

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x = df["Établissement"],
        y = df[df.columns[colonne_à_afficher]],
        name = df.columns[colonne_à_afficher],
    ) 
)
    
fig.add_trace(
    go.Bar(
        x = df["Établissement"],
        y = (100 - df[df.columns[75]]), # Comme on a accès qu'au pourcentage de filles
        name = "% d’admis dont garçons",
    ) 
)

fig.update_layout(title="Proportion Filles/Garçons (%)",
                  barmode='stack'
)

fig.show()

colonnes_à_afficher = [85,81,82,83,84,86] # Colonnes relatives au pourcentage des mentions

fig = go.Figure()
for i in colonnes_à_afficher:
  fig.add_trace(
      go.Bar(
          x = df["Établissement"],
          y = df[df.columns[i]],
          name = df.columns[i],
      )
)
  
fig.update_layout(title="Proportion des mentions obtenues par les admis",
                  barmode='stack',
                  xaxis={'categoryorder':''}
)

fig.show()

"""# **À vous de jouer ! ✌️**

> Avec les quelques exemples présentés précédemment, vous devriez pouvoir vous amuser comme vous voulez en modifiant le code proposé.
> 
> J'essaierai l'an prochain de faire d'ajouter des graphes en récupérant les données sur plusieurs années.
"""