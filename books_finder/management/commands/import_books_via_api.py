import json
import os
import re
import time
from datetime import date
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.core.management.base import BaseCommand, CommandError
from dotenv import load_dotenv

from books_finder.models import Author, Book, Tag, Theme

load_dotenv()

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
API_URL = "https://www.googleapis.com/books/v1/volumes"
PAGE_SIZE = 40  # Maximum allowed by the API
MAX_PAGES = 5  # Stop looking for a theme after this many pages


class Command(BaseCommand):
    help = "Import books and authors from the Google Books API for every theme in the database"

    def add_arguments(self, parser):
        parser.add_argument("--per-theme", type=int, default=20, help="Number of books to import per theme (default: 20)")
        parser.add_argument("--since", type=int, default=1980, help="Ignore books published before this year (default: 1980)")
        parser.add_argument("--lang", default="fr", help="Language of the books (default: fr)")

    def handle(self, *args, **options):
        if not GOOGLE_BOOKS_API_KEY:
            raise CommandError("GOOGLE_BOOKS_API_KEY is missing from the .env file.")

        themes = list(Theme.objects.all())
        if not themes:
            raise CommandError("No theme in the database, run `python manage.py init_db` first.")

        # Tag names are searched as whole words in the title and description of each book
        # (hyphens count as part of a word so that "Aide-mémoire" does not match the "Mémoire" tag)
        tag_patterns = [
            (tag, re.compile(rf"(?<![\w-]){re.escape(tag.name)}(?![\w-])", re.IGNORECASE))
            for tag in Tag.objects.all()
        ]

        total = 0
        for theme in themes:
            created = self._import_theme(theme, tag_patterns, options)
            total += created
            self.stdout.write(f"{theme.name}: {created} books imported")

        self.stdout.write(self.style.SUCCESS(f"{total} books imported ({Author.objects.count()} authors in database)."))

    def _import_theme(self, theme, tag_patterns, options):
        created = 0
        for page in range(MAX_PAGES):
            items = self._fetch(theme.name, page * PAGE_SIZE, options["lang"])
            if not items:
                break

            for item in items:
                book_data = self._parse(item["volumeInfo"], options["since"], options["lang"])
                if book_data is None:
                    continue

                author, _ = Author.objects.get_or_create(name=book_data.pop("author"))
                book = Book.objects.filter(title__iexact=book_data["title"], author=author).first()
                if book:
                    book.theme.add(theme)  # Already imported, possibly from another theme
                    continue

                book = Book.objects.create(author=author, **book_data)
                book.theme.add(theme)
                text = f"{book.title} {book.description}"
                book.tags.set([tag for tag, pattern in tag_patterns if pattern.search(text)])

                created += 1
                if created >= options["per_theme"]:
                    return created
        return created

    def _fetch(self, query, start_index, lang):
        '''
        Return one page of volumes from the Google Books API.
        '''
        params = urlencode({
            "q": query,
            "langRestrict": lang,
            "printType": "books",
            "startIndex": start_index,
            "maxResults": PAGE_SIZE,
            "key": GOOGLE_BOOKS_API_KEY,
        })

        for attempt in range(3):
            try:
                with urlopen(f"{API_URL}?{params}", timeout=20) as response:
                    return json.load(response).get("items", [])
            except HTTPError as error:
                if error.code != 429 and error.code < 500:
                    raise CommandError(f"Google Books API error {error.code}: {error.read().decode()}")
                self.stderr.write(f"Google Books API error {error.code}, retrying...")
            except (URLError, TimeoutError) as error:
                self.stderr.write(f"Network error: {error}, retrying...")
            time.sleep(2 ** attempt)  # Wait before retrying (rate limit or server error)

        # Skip the rest of this query instead of stopping the whole import
        self.stderr.write(self.style.WARNING(f"Giving up on \"{query}\" at index {start_index}."))
        return []

    def _parse(self, info, since, lang):
        '''
        Convert a Google Books volume into Book fields.
        Return None if the volume lacks an author, a usable publication date or is in another language
        (langRestrict alone still lets some foreign books through).
        '''
        authors = info.get("authors")
        publication_date = self._parse_date(info.get("publishedDate", ""))
        if (
            not authors
            or not info.get("title")
            or info.get("language") != lang
            or publication_date is None
            or publication_date.year < since
        ):
            return None

        title = info["title"]
        if info.get("subtitle"):
            title = f"{title} : {info['subtitle']}"

        return {
            "title": title[:200],
            "author": authors[0][:100],
            "description": info.get("description", ""),
            "publication_date": publication_date,
        }

    def _parse_date(self, value):
        '''
        Google Books dates can be "2021", "2021-03" or "2021-03-15".
        '''
        try:
            parts = [int(part) for part in value.split("-")]
            return date(*parts, *[1] * (3 - len(parts)))
        except (ValueError, TypeError):
            return None
