# Fichiers présents dans le projet
- database_creation.ipynb
- main.py
- test_serveur.py
- Dockerfile
- Docker-compose.yml
   
- data/
-   employees.csv
-   sales.csv
-   employees_clean.csv
-   sales_clean.csv 


# Étapes réalisées
## 1. Ingérer les données
- Tout a été réalisé.
Voir dans le fichier database_creation.ipynb. Ce fichier prend en entrée les fichiers csv de data (fourni dans le gitlab) pour les traiter.
J'ai fait le choix de faire une **base de données** sur MySQL que j'ai appelé 'dataswati_test'. J'ai fait ce choix, car l'importation de fichier csv sur MySQL est facile et que c'est un système de gestion de database avec lequel je suis particulièrement familier.
Pour l'exploitation des données, j'ai utilisé la library 'pandas', j'ai supprimé les doublons tout en conservant les lignes avec des valeurs manquantes et pour finir, j'ai ajouté une colonnes **PrixRéel**.

**_NOTE:_** J'ai modifié le nom de certaines colonnes pour ne pas à avoir à travailler avec des accents (pour ne pas rencontrer de problème entre les normes UTF-8 et Ascii).

## 2. Créer une API avec FastAPI
- Tout a été réalisés
Voir le fichier main.py. Ce fichier créé l'API avec FastAPI et fait le lien avec la database MySQL.
Ce fichier permet de téléverser un fichier csv dans la database (dans la mesure où la database est déjà existante). Il applique seulement la règle de la suppression des doublons puisque toutes les autres contraintes étaient propre aux fichiers csv du projet.
L'API permet notamment de:
- trouver une vente(sales) ou un employé(employees) selon son ID
- trouver les ventes(sales) selon une catégorie choisie pour le user et retourner seulement les colonnes selectionnées
- trouver les ventes(sales) comprises entre deux dates et retourner seulement les colonnes sélectionnées
- trouver le chiffre d'affaires journalier par vendeur
- ajouter une seule vente
- ajouter un fichier csv

### Lien pour tester l'API (une fois lancée):
http://127.0.0.1:8000/ <br>
http://127.0.0.1:8000/employees/1 <br>
http://127.0.0.1:8000/sales/1 <br>
http://127.0.0.1:8000/sales_categorie/Informatique <br>
http://127.0.0.1:8000/sales_in_date_range?start_date=2023-10-01&end_date=2023-10-31 <br>
http://127.0.0.1:8000/sales_revenue_per_day_and_vendeur <br>
+++

**_NOTE:_** J'ai ajouter un fichier de test unitaire pour vérifier que les fonctions implémentées fonctionnent correctement.
**_NOTE:_** Les fonctions qui permettent de modifier la base de données 'ajouter une vente', 'ajouter un fichier csv' ne fonctionnent pas en utilisant une url sur internet (erreur 405) mais elles fonctionnent correctement avec les tests unitaires, elle modifie la database

## 3. Conteneuriser la solution
- Tout a été réalisés
Voir les fichiers Dockerfile et Docker-compose.yml. Toutes les fonctionnalités citées dans l'étape 2 fonctionnent (mais on rencontre le même problème pour les modifications de la database via un url sur Internet.)

## 4. Rédiger une documentation
- Tout a été réalisés
Voir le README.md et les fichiers python sont commentés.

## 5. Bonus (optionnel)
- Je n'ai réalisé que les tests unitaires en bonus

# Mise en place du projet
## Etape 1:
#### Création d'une database MySQL: 'dataswati_test': <br>
 - CREATE DATABASE dataswati_test; <br>
#### Lancer le fichier database_creation.ipynb et exécuter toutes les cellules <br>
####  Importer les fichiers csv dans la database: <br>
 - Utiliser PhpMyAdmin ou alors via la console <br>

## Etape 2
#### Emplacement du fichier main.py: <br>
 - project_dataswati/venv/Scripts/main.py<br>
#### Emplacement du fichier des test unitaire:<br>
 - project_dataswati/venv/Scripts/test_server.py<br>
#### Prérequis pour lancer les fichiers:<br>
#### main<br>
#### dans le terminal - .../venv/Scripts:<br>
#### pour activer l'environnement virtuel:<br>
 - ./activate<br>
#### Installer les libraries<br>
 - pip install fastapi uvicorn mysql.connector pydantic requests<br>
#### Veiller à ce que votre "config" dans le main ait bien:
 - 'host': '127.0.0.1' décommenté et #'host': 'host.docker.internal' commenté
#### Lancer le serveur (le serveur se lancera en localhost: 127.0.0.1:8000):<br>
 - uvicorn main:app --reload --port 8000<br>
#### test_serveur<br>
#### dans un autre terminal - ../venv/Scripts:<br>
#### lancer les tests unitaires:<br>
 - python test_serveur.py<br>
#### Pour désactiver l'environnement virtuel:<br>
 - ./deactivate<br>

## Etape 3
#### Veiller à ce que votre "config" dans le main ait bien:
 - #'host': '127.0.0.1' commenté et 'host': 'host.docker.internal' décommenté
#### Dans le terminal - .../venv/Scripts:<br>
 - docker-compose up --build<br>
#### Lancer l'API - sur le browser:<br>
 - localhost:8000<br>

**_NOTE:_** Vérifier dans les fichiers Docker que les informations soit les bonnes particulièrement le nom de la database MySQL et les login à votre MySQL

# Remarque
J'ai apprécié sur ce projet, avec plus de temps, j'y aurais ajouté d'autres fonctionnalités: plus d'options dans l'API(delete & modify), j'aurais également aimé faire une API propre avec streamlit notamment.
Pour les autres bonus, il m'aurait fallu me renseigner dessus pour pouvoir les réaliser.


