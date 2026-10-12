# Biblits

Biblits est un moteur de recherche de livres pour les étudiants et professionnels du travail social (éducation spécialisée, protection de l'enfance, handicap…). On peut chercher un livre par titre, auteur, thème ou tag, ou parcourir les thèmes.

L'objectif ici est de créer un moteur de recherche simple pour faciliter l'accès aux livres pertinents pour les étudiants et professionnels du travail social.

## Fonctionnement

Biblits est une application web développée avec Python et Django.
La base de donnée est PostgreSQL.
L'application utilise l'API Google Books pour récupérer les informations sur les livres.

### Environnement

Pour faire fonctionner l'application, il faut créer un fichier `.env` à la racine du projet avec les variables suivantes :

```
DB_PASSWORD=mot_de_passe_de_la_base
GOOGLE_BOOKS_API_KEY=clé_api_google_books
```

### Initialisation

Pour initialiser la base de données, il faut exécuter les commandes suivantes :

```bash
python manage.py init_db                  # Supprime tout puis crée les thèmes et les tags
python manage.py import_books_via_api     # Importe des livres depuis l'API Google

```
