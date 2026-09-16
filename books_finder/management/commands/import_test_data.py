import random
from datetime import date

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from books_finder.models import Author, Book, Tag, Theme

# Library themes, each with plausible book titles
TITLES_BY_THEME = {
    "Psychologie": [
        "Psychologie du développement de l'enfant",
        "Introduction à la psychopathologie",
        "La théorie de l'attachement",
        "Comprendre les troubles anxieux",
        "Psychologie de l'adolescent",
        "Le traumatisme psychique",
        "Clinique du lien",
        "Les mécanismes de défense",
    ],
    "Sociologie": [
        "Sociologie de la famille",
        "Les inégalités sociales en France",
        "Sociologie de l'exclusion",
        "Précarité et pauvreté",
        "Jeunesses populaires",
        "Vivre dans les quartiers prioritaires",
        "Les classes sociales aujourd'hui",
        "Migrations et société",
    ],
    "Éducation spécialisée": [
        "Le métier d'éducateur spécialisé",
        "La relation éducative",
        "L'accompagnement éducatif au quotidien",
        "Le projet personnalisé",
        "Écrits professionnels en éducation spécialisée",
        "L'éducateur et le groupe",
        "Pratiques éducatives en internat",
        "La posture professionnelle",
    ],
    "Handicap": [
        "Handicap et inclusion",
        "Accompagner les personnes autistes",
        "Le polyhandicap",
        "Handicap psychique et vie sociale",
        "L'autodétermination des personnes handicapées",
        "Déficience intellectuelle et accompagnement",
        "Vieillir avec un handicap",
        "L'école inclusive",
    ],
    "Protection de l'enfance": [
        "La protection de l'enfance en France",
        "L'enfant placé",
        "Maltraitance et négligences",
        "Le signalement d'enfant en danger",
        "L'accueil familial",
        "Les mineurs non accompagnés",
        "Parentalité et soutien aux familles",
        "L'aide sociale à l'enfance",
    ],
    "Droit et politiques sociales": [
        "Droit de l'action sociale",
        "Les politiques sociales",
        "Le droit des usagers",
        "Droit de la famille",
        "Protection sociale et solidarités",
        "La loi 2002-2 et les droits des usagers",
        "Les politiques du handicap",
        "Décentralisation et action sociale",
    ],
    "Santé et addictions": [
        "Addictions et conduites à risque",
        "La réduction des risques",
        "Santé mentale et précarité",
        "Alcool et dépendances",
        "Soigner et accompagner en addictologie",
        "Les jeunes face aux drogues",
        "Santé communautaire",
        "Addictions sans substance",
    ],
    "Éthique et déontologie": [
        "Éthique du travail social",
        "Le secret professionnel",
        "Déontologie et responsabilité",
        "Les dilemmes éthiques en travail social",
        "Bientraitance et qualité de l'accompagnement",
        "Le consentement de la personne accompagnée",
        "Le secret partagé",
        "Éthique du care",
    ],
    "Communication": [
        "La communication non violente",
        "L'entretien d'aide",
        "Écouter et accompagner",
        "La gestion des conflits",
        "Communication et handicap",
        "Médiation et communication interculturelle",
        "Communiquer avec les familles",
        "La relation d'aide",
    ],
    "Méthodologie de projet": [
        "Méthodologie du projet social",
        "Conduire un projet en action sociale",
        "Le diagnostic de territoire",
        "Évaluer un projet",
        "Piloter un projet d'établissement",
        "Le développement social local",
        "Méthodologie de l'intervention sociale",
        "Monter un projet associatif",
    ],
    "Travail en équipe et institutions": [
        "Le travail en équipe pluridisciplinaire",
        "L'analyse des pratiques professionnelles",
        "Les institutions sociales et médico-sociales",
        "Le partenariat en action sociale",
        "Manager une équipe en établissement social",
        "La réunion d'équipe",
        "Souffrance au travail et épuisement professionnel",
        "Dynamique des groupes et institutions",
    ],
    "Recherche et sciences sociales": [
        "Initiation à la recherche en travail social",
        "Méthodes d'enquête en sciences sociales",
        "Rédiger un mémoire en travail social",
        "L'entretien de recherche",
        "L'observation participante",
        "Analyser des données qualitatives",
        "Épistémologie des sciences sociales",
        "Construire un questionnaire d'enquête",
    ],
}

SUBTITLES = [
    "Repères pour la pratique",
    "Théories et pratiques",
    "Enjeux et perspectives",
    "Approches cliniques",
    "Guide à l'usage des professionnels",
    "Concepts et méthodes",
    "Nouvelles approches",
    "Du diagnostic à l'intervention",
]

# Every book gets one format tag and up to two topic tags
FORMAT_TAGS = ["Manuel", "Guide pratique", "Essai", "Témoignage", "Ouvrage collectif", "Étude de cas"]
TOPIC_TAGS = [
    "Petite enfance",
    "Adolescence",
    "Personnes âgées",
    "Familles",
    "Autisme",
    "Précarité",
    "Insertion",
    "Migration",
    "Violences",
    "Médiation",
    "Préparation DEES",
    "Préparation DEASS",
    "Préparation DEME",
]


class Command(BaseCommand):
    help = "Generate realistic test data for themes, tags, authors and books"

    def add_arguments(self, parser):
        parser.add_argument("--books", type=int, default=60, help="Number of books to create (default: 60)")
        parser.add_argument("--authors", type=int, default=20, help="Number of authors to create (default: 20)")
        parser.add_argument("--seed", type=int, help="Seed to generate the same data on every run")
        parser.add_argument("--clear", action="store_true", help="Delete all books, authors, themes and tags first")

    @transaction.atomic
    def handle(self, *args, **options):
        if options["authors"] < 1 or options["books"] < 0:
            raise CommandError("--authors must be at least 1 and --books cannot be negative.")

        rng = random.Random(options["seed"])
        fake = Faker("fr_FR")
        if options["seed"] is not None:
            fake.seed_instance(options["seed"])

        if options["clear"]:
            Book.objects.all().delete()
            Author.objects.all().delete()
            Theme.objects.all().delete()
            Tag.objects.all().delete()
            self.stdout.write("Existing data deleted.")

        themes = {name: Theme.objects.get_or_create(name=name)[0] for name in TITLES_BY_THEME}
        format_tags = [Tag.objects.get_or_create(name=name)[0] for name in FORMAT_TAGS]
        topic_tags = [Tag.objects.get_or_create(name=name)[0] for name in TOPIC_TAGS]

        authors = self._create_authors(fake, options["authors"])
        # Each author specialises in one or two themes, so their books stay consistent
        specialties = {author.pk: rng.sample(list(themes), k=rng.randint(1, 2)) for author in authors}

        used_titles = set(Book.objects.values_list("title", flat=True))
        title_pools = self._build_title_pools(rng, used_titles)

        created = 0
        for _ in range(options["books"]):
            author = rng.choice(authors)
            theme_name = rng.choice(specialties[author.pk])
            title = next(title_pools[theme_name], None)
            if title is None:
                continue  # Every title of this theme is already taken

            book = Book.objects.create(
                title=title,
                author=author,
                publication_date=fake.date_between(start_date=date(1990, 1, 1), end_date="today"),
            )

            book_themes = [themes[theme_name]]
            if rng.random() < 0.3:
                book_themes.append(rng.choice([t for name, t in themes.items() if name != theme_name]))
            book.theme.set(book_themes)
            book.tags.set([rng.choice(format_tags), *rng.sample(topic_tags, k=rng.randint(0, 2))])
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created} books and {len(authors)} authors "
            f"({len(themes)} themes and {len(format_tags) + len(topic_tags)} tags available)."
        ))

    def _create_authors(self, fake, count):
        names = []
        while len(names) < count:
            name = f"{fake.first_name()} {fake.last_name()}"
            if name not in names:
                names.append(name)
        return [Author.objects.create(name=name) for name in names]

    def _build_title_pools(self, rng, used_titles):
        '''
        Return an iterator of unused titles for each theme.
        Base titles come first (some with a subtitle), then extra subtitled variants.
        '''
        pools = {}
        for theme_name, bases in TITLES_BY_THEME.items():
            first = [f"{base} : {rng.choice(SUBTITLES)}" if rng.random() < 0.4 else base for base in bases]
            extra = [f"{base} : {subtitle}" for base in bases for subtitle in SUBTITLES]
            rng.shuffle(first)
            rng.shuffle(extra)
            titles = dict.fromkeys(first + extra)  # Removes duplicates while keeping order
            pools[theme_name] = iter([title for title in titles if title not in used_titles])
        return pools
