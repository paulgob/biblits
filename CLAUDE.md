# Biblits

Moteur de recherche de livres pour les étudiants et professionnels du travail social (éducation spécialisée, protection de l'enfance, handicap…). On cherche un livre par titre, auteur, thème ou tag, ou on parcourt les thèmes.

## Stack

- Python / Django 6.1 / PostgreSQL (via psycopg 3)
- HTML (templates Django) / CSS pur, sans framework ni JavaScript
- Faker pour les données de test, python-dotenv pour les secrets
- Aucune nouvelle dépendance sans validation préalable. Si une est validée, l'ajouter à `requirements.txt`.

## Structure

- `biblits/` : configuration du projet (`settings.py`, `urls.py`).
- `books_finder/` : l'unique app.
  - `models.py` : `Book`, `Author`, `Theme`, `Tag`. Un livre a un auteur, plusieurs thèmes (`theme`, au singulier) et plusieurs tags. Le slug d'un thème est généré automatiquement depuis son nom.
  - `services.py` : `search_books()`, recherche plein texte PostgreSQL (config `french`, recherche par préfixe sur chaque mot, pondération titre/auteur > thèmes/tags).
  - `views.py` / `urls.py` : vues fonctionnelles. `login`, `register` et `favorites` ne sont pas encore implémentées (elles affichent `in-progress.html`).
  - `templates/books_finder/` : toutes les pages étendent `base.html` (menu latéral `<aside>` + footer). `index.html` masque le menu en surchargeant `{% block menu %}`.
  - `static/books_finder/` : `style.css` (feuille unique), police Roboto, images.
  - `management/commands/` : commandes d'initialisation de la base (voir ci-dessous).
- `.env` : secrets (`DB_PASSWORD`, `GOOGLE_BOOKS_API_KEY`). Ne jamais afficher, copier ou committer son contenu.
- `memo.txt` : notes personnelles contenant des identifiants. Ne jamais recopier son contenu ailleurs.

## Commandes utiles

```bash
python manage.py runserver
python manage.py makemigrations && python manage.py migrate
python manage.py check

# Données (init_db et import_test_data --clear VIDENT la base : demander avant de les lancer)
python manage.py init_db                  # Supprime tout puis crée les thèmes et les tags
python manage.py import_books_via_api     # Importe des livres depuis l'API Google Books pour chaque thème
python manage.py import_test_data         # Génère de faux livres et auteurs avec Faker
```

## Conventions

### Général

- Contenu visible par l'utilisateur en français. Code, noms de variables, commentaires et docstrings en anglais.
- Docstrings entre `'''`, commentaires courts en fin de ligne quand c'est utile : suivre le style existant.
- Logique métier ou requêtes complexes dans `services.py`, pas dans les vues.
- La recherche repose sur des fonctionnalités propres à PostgreSQL (`django.contrib.postgres`) : ne pas proposer SQLite.
- Toute modification d'un modèle s'accompagne de sa migration (`makemigrations`). Ne jamais modifier une migration existante.
- Le menu et le footer sont dans `base.html` : les modifier là, jamais dans les pages enfants.
- Messages de commit : `Feat: …`, `Fix: …`, `UI: …`, en anglais, à l'impératif.

### CSS

- Le plus simple possible : le moins de CSS nécessaire pour obtenir l'effet voulu.
- Ne pas modifier la structure HTML des pages, sauf pour ajouter des classes ou des IDs.
- N'ajouter des classes ou IDs que si c'est nécessaire. Privilégier les classes existantes ou les sélecteurs HTML (`form input`, `.search-form input`).
- Utiliser les variables CSS de la palette (`:root` dans `style.css`). Ajouter une variable plutôt qu'une couleur en dur.
- Accessibilité de base : balises sémantiques, `alt` sur les images, `aria-label` sur les boutons sans texte, contrastes suffisants.

## Méthode de travail

- Lis `lessons.md` avant de commencer.
- Si la demande est ambiguë, pose une question avant de coder.
- Si quelque chose ne se passe pas comme prévu : arrête-toi, explique le problème et propose un nouveau plan avant de continuer.
- Ne modifie que ce qui est demandé. Signale les améliorations possibles sans les appliquer.
- Ne lance jamais une commande qui supprime des données de la base sans accord explicite.

## Principes

- Simplicité d'abord : la solution la plus simple, avec le moins de code modifié possible.
- Corriger la cause, pas le symptôme : pas de rustine temporaire. Si la vraie correction dépasse le périmètre demandé, dis-le.
- Utiliser ce que Django fournit déjà (`get_object_or_404`, ORM, `{% url %}`, `{% static %}`) plutôt que de le réécrire.

## Définition de « terminé »

- `python manage.py check` ne signale aucune erreur.
- Les migrations sont créées et appliquées si les modèles ont changé.
- Les pages concernées s'affichent sans erreur (serveur et console du navigateur).
- Tous les liens internes fonctionnent (toujours via `{% url %}`).
- Les tests passent (`python manage.py test`) s'il en existe pour la partie modifiée.

## Points connus (à ne pas corriger sans demande)

- Le site n'est pas encore responsive (menu latéral fixe de 220px).
- `tests.py` est vide.
- `SECRET_KEY` est en dur dans `settings.py` et `DEBUG = True` : configuration de développement uniquement.

## Apprentissage continu

Après chaque correction de ma part, ajoute une règle dans `lessons.md` (crée-le s'il n'existe pas) :

- une ligne par règle, formulée comme une consigne (« Toujours… » / « Ne jamais… ») ;
- pas de doublon : reformule une règle existante plutôt que d'en ajouter une proche.
