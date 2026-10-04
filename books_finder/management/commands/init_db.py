from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from books_finder.models import Author, Book, Tag, Theme

THEMES = [
    "Psychologie",
    "Sociologie",
    "Éducation spécialisée",
    "Handicap",
    "Protection de l'enfance",
    "Droit et politiques sociales",
    "Santé et addictions",
    "Éthique et déontologie",
    "Communication",
    "Méthodologie de projet",
    "Travail en équipe et institutions",
    "Recherche et sciences sociales",
]

TAGS = [
    # Type d'ouvrage
    "Manuel",
    "Guide pratique",
    "Essai",
    "Témoignage",
    "Ouvrage collectif",
    "Étude de cas",
    "Dictionnaire",
    "Fiches de révision",
    "Annales",
    "Classique",
    # Public
    "Petite enfance",
    "Enfance",
    "Adolescence",
    "Jeunes majeurs",
    "Adultes",
    "Personnes âgées",
    "Familles",
    "Parentalité",
    "Mineurs non accompagnés",
    "Personnes sans domicile",
    "Personnes détenues",
    # Handicap et santé mentale
    "Autisme",
    "TDAH",
    "Déficience intellectuelle",
    "Polyhandicap",
    "Handicap psychique",
    "Troubles du comportement",
    "Troubles dys",
    "Santé mentale",
    "Psychiatrie",
    "Addictions",
    "Vieillissement",
    "Maladie d'Alzheimer",
    # Problématiques sociales
    "Précarité",
    "Exclusion",
    "Insertion",
    "Migration",
    "Interculturalité",
    "Violences",
    "Violences conjugales",
    "Maltraitance",
    "Harcèlement",
    "Délinquance",
    "Radicalisation",
    "Discriminations",
    "Genre",
    "Laïcité",
    # Psychologie
    "Attachement",
    "Traumatisme",
    "Résilience",
    "Développement de l'enfant",
    "Psychanalyse",
    "Approche systémique",
    "Thérapies cognitives et comportementales",
    "Neurosciences",
    "Émotions",
    # Pratiques professionnelles
    "Relation d'aide",
    "Accompagnement",
    "Médiation",
    "Écoute",
    "Entretien",
    "Observation",
    "Écrits professionnels",
    "Projet personnalisé",
    "Travail de groupe",
    "Travail avec les familles",
    "Médiation animale",
    "Activités éducatives",
    "Analyse des pratiques",
    "Supervision",
    "Posture professionnelle",
    "Secret professionnel",
    "Bientraitance",
    "Épuisement professionnel",
    "Pouvoir d'agir",
    "Autodétermination",
    "Inclusion",
    # Cadre institutionnel
    "ASE",
    "PJJ",
    "MECS",
    "IME",
    "ESAT",
    "EHPAD",
    "CHRS",
    "MDPH",
    "Loi 2002-2",
    "Loi 2005",
    # Formation
    "Préparation DEES",
    "Préparation DEASS",
    "Préparation DEME",
    "Préparation DEEJE",
    "Préparation DEAES",
    "Préparation CAFERUIS",
    "Stage",
    "Mémoire",
]

# CLEAR THE DATABASE

class Command(BaseCommand):
    help = "Initializes the database with themes and tags"

    def handle(self, *args, **options):
        Book.objects.all().delete()
        Author.objects.all().delete()
        Theme.objects.all().delete()
        Tag.objects.all().delete()

        for theme_name in THEMES:
            Theme.objects.create(name=theme_name)

        for tag_name in TAGS:
            Tag.objects.create(name=tag_name)

        self.stdout.write(self.style.SUCCESS("Database initialized with themes and tags."))

    