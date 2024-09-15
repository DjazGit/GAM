import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import openpyxl



# Charger les données géographiques
algeria_map = gpd.read_file("C:\\Users\\HONOR-ECC\\Downloads\\all-wilayas_modified.geojson")

# Charger les données climatiques
covid_algeria = pd.read_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\Data\\covid_algeria.csv")

# Nettoyer les noms des villes
algeria_map['name'] = algeria_map['name'].str.lower().str.strip()
covid_algeria['CITY'] = covid_algeria['CITY'].str.lower().str.strip()

# Convertir la colonne 'Date' en datetime
covid_algeria['Date'] = pd.to_datetime(covid_algeria['Date'])

# Extraire l'année de la date
covid_algeria['Year'] = covid_algeria['Date'].dt.year



# Calculer les limites de l'écart interquartile (IQR)
Q1 = covid_algeria[['MXT', 'MNT', 'AT']].quantile(0.25)
Q3 = covid_algeria[['MXT', 'MNT', 'AT']].quantile(0.75)
IQR = Q3 - Q1

# Définir les bornes pour filtrer les valeurs aberrantes
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Filtrer les valeurs aberrantes
covid_algeria_filtered = covid_algeria[
    (covid_algeria['MXT'] >= lower_bound['MXT']) & (covid_algeria['MXT'] <= upper_bound['MXT']) &
    (covid_algeria['MNT'] >= lower_bound['MNT']) & (covid_algeria['MNT'] <= upper_bound['MNT']) &
    (covid_algeria['AT'] >= lower_bound['AT']) & (covid_algeria['AT'] <= upper_bound['AT'])
]

# Réinitialiser l'index
covid_algeria_filtered.reset_index(drop=True, inplace=True)


#

#############################################################
#########MXT
# Sélectionner les colonnes nécessaires
covid_algeria_mxt = covid_algeria[['Year', 'CITY', 'MXT']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_mxt.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map(year, data, geo_data, column, title, cmap='coolwarm'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température maximale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Température maximale moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

 # Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map(year, annual_means, algeria_map, 'MXT', f"Température maximale (C°) moyenne par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\mxt_annual_means.csv", index=False)   

##################################################################################################################################################################"""
######MNT 
# Sélectionner les colonnes nécessaires

covid_algeria_mnt = covid_algeria[['Year', 'CITY', 'MNT']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_mnt.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map_mnt(year, data, geo_data, column, title, cmap='coolwarm'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température minimale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Température minimale moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

# Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map_mnt(year, annual_means, algeria_map, 'MNT', f"Température minimale (C°) moyenne par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\mnt_annual_means.csv", index=False)


##################################################################################################################################################################"""
######AT
# Sélectionner les colonnes nécessaires
covid_algeria_AT = covid_algeria[['Year', 'CITY', 'AT']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_AT.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map_mnt(year, data, geo_data, column, title, cmap='Oranges'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température minimale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Température moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

# Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map_mnt(year, annual_means, algeria_map, 'AT', f"Température moyenne (C°) par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\AT_annual_means.csv", index=False)

##################################################################################################################################################################"""
######HM
# Sélectionner les colonnes nécessaires
covid_algeria_hm = covid_algeria[['Year', 'CITY', 'HM']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_hm.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map_mnt(year, data, geo_data, column, title, cmap='plasma'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température minimale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Humidité  moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

# Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map_mnt(year, annual_means, algeria_map, 'HM', f"Humidité (%) moyenne par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\HM_annual_means.csv", index=False)

##################################################################################################################################################################"""
##################################################################################################################################################################"""
######RF
# Sélectionner les colonnes nécessaires
covid_algeria_rf = covid_algeria[['Year', 'CITY', 'RF']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_rf.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map_mnt(year, data, geo_data, column, title, cmap='Blues'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température minimale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Précipitations moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

# Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map_mnt(year, annual_means, algeria_map, 'RF', f"Précipitations (mm) moyenne par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\RF_annual_means.csv", index=False)

##################################################################################################################################################################"""
##################################################################################################################################################################"""
######WS
# Sélectionner les colonnes nécessaires
covid_algeria_ws = covid_algeria[['Year', 'CITY', 'WS']]

# Calculer la moyenne annuelle pour chaque ville
annual_means = covid_algeria_ws.groupby(['Year', 'CITY']).mean().reset_index()

def plot_map_mnt(year, data, geo_data, column, title, cmap='winter'):
    # Joindre les données géographiques avec les moyennes annuelles
    map_data = geo_data.merge(data[data['Year'] == year], left_on='name', right_on='CITY', how='left')
    
    # Créer une carte choroplèthe pour la température minimale moyenne
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    
    # Tracer les données avec une coloration correspondant à la colonne spécifiée
    map_data.plot(column=column, ax=ax, legend=True,
                  legend_kwds={'label': "Vitesse du vent moyenne",
                               'orientation': "horizontal"},
                  cmap=cmap)
    
    # Filtrer les villes sans données climatiques
    empty_cities = map_data[map_data[column].isna()]
    empty_cities.plot(ax=ax, color='lightgray', alpha=0.5)  # Cartographier les villes sans données en gris clair
    # Ajouter un titre
    ax.set_title(title)
    # Afficher la carte
    plt.show()

# Générer les cartes pour chaque année
years = [2020, 2021, 2022]
for year in years:
    plot_map_mnt(year, annual_means, algeria_map, 'WS', f"Vitesse du vent (Km/h) moyenne par ville en Algérie ({year})")

# Sauvegarder les moyennes annuelles dans un fichier CSV
annual_means.to_csv("C:\\Users\\HONOR-ECC\\Desktop\\These de doctorat\\These\\Chapitre 3 Covid_19 et Qualité de l'air\\RF_annual_means.csv", index=False)



