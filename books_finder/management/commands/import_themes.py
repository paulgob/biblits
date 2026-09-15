import csv
from django.core.management.base import BaseCommand
from books_finder.models import Theme

class Command(BaseCommand):
    help = "Importe les thèmes depuis le CSV"

    def handle(self, *args, **options):
        with open("data/csv/themes_its.csv", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):        # a line = {'name': 'Science Fiction'}
                Theme.objects.get_or_create(name=row["name"])