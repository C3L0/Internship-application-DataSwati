# Contexte
Vous êtes data-engineer dans une équipe tech.
Vous êtes chargés de développer un script d'ingestion et une **API REST**.

Le script d'ingestion a pour but d'ingérer des fichiers csv en base de données. 
L'API REST a pour but d'ingérer des nouvelles données, d'extraire des données existantes et de fournir des statistiques.


# Données

### Fichier **`sales.csv`** :
- `ID` : Identifiant unique de la transaction.
- `Date` : Date de la vente.
- `Produit` : Nom du produit vendu.
- `Prix` : Prix unitaire du produit.
- `Quantité` : Quantité d'unités vendues.
- `Catégorie` : Catégorie du produit (Informatique, Accessoires, etc.).
- `Remise` : Pourcentage de réduction appliqué sur la transaction.
- `Vendeur` : Identifiant du vendeur ayant effectué la transaction.

### Fichier **`employees.csv`** :
- `ID` : Identifiant unique du vendeur.
- `Nom` : Nom du vendeur.
- `Équipe` : Équipe à laquelle appartient le vendeur.

# Étapes à réaliser

## 1. Ingérer les données
- Enregistrer les données des fichiers CSV dans une **base de données** de votre choix (PostgreSQL, MySQL, MongoDB, etc.).
- Le modèle de données doit être conçu de manière à faciliter l'exploitation des informations.
- Les lignes duppliquées doivent être ignorées.
- Les lignes contenant des valeurs manquantes doivent être quand même importées.
- Ajouter une colonne calculée : **PrixRéel** qui correspond à `Prix * Quantité`, en déduisant le pourcentage de remise.

**_NOTE:_** Le script doit être écrit python.


## 2. Créer une API avec FastAPI
- L'API doit permettre aux utilisateurs de **téléverser un fichier CSV** pour ajouter de nouvelles données à la base de données. Les mêmes règles que pour l'ingestion initiale s'appliquent.
- L'API doit offrir la possibilité de **consulter les données** sous forme de JSON avec des **filtres personnalisés**, tels que :
  - Colonnes spécifiques à inclure dans la réponse.
  - Intervalle de dates.
  - Catégories de produits.
- L'API doit inclure une route permettant de **consulter le chiffre d'affaires par jour et par vendeur**.

## 3. Conteneuriser la solution
- **Conteneuriser l'API** ainsi que la base de données en utilisant Docker. Le projet doit pouvoir être facilement déployé via **Docker Compose**.

## 4. Rédiger une documentation
- Rédiger une **documentation concise** expliquant comment déployer le projet et décrivant les principales fonctionnalités implémentées.

## 5. Bonus (optionnel)
Vous êtes libre d'ajouter des fonctionnalités supplémentaires que vous jugez pertinentes. Voici quelques idées d'améliorations possibles :
- Ajouter des **tests unitaires** pour valider les fonctionnalités de l'API.
- Créer de nouvelles routes pour enrichir l'API (par exemple, pour récupérer des statistiques plus détaillées).
- **Supporter d'autres types de fichiers** pour l'ingestion, comme JSON ou XML.
- Mettre en place une **pipeline CI/CD** pour automatiser les tests et la construction de l'image.
- Ajouter un système d'**authentification** pour sécuriser les accès à l'API.


## Information

- **Structuration du projet** : Le projet doit être bien organisé
- **Qualité et lisibilité du code** : Le code doit être propre, lisible et respecter les bonnes pratiques de développement.
- Le livrable doit être un lien vers GitHub, GitLab, ou une autre plateforme de gestion de code.
