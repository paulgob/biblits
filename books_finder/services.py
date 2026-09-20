from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    Lexeme,
)
from functools import reduce
import operator
from django.db.models import StringAgg, Value

from .models import Book


def search_books(search_term):
    '''
    Search for books based on the provided search term.
    The search is performed on the title, author name, theme names, and tag names.
    '''

    # Trim whitespace from the search term
    search_term = search_term.strip()

    if not search_term:
        return Book.objects.none()

    # Field configuration
    # Many-to-many fields are aggregated into a single string, otherwise their
    # joins would return one row per (theme, tag) combination for each book
    vector = (
        SearchVector(
            "title",
            weight="A",
            config="french"
        )
        +
        SearchVector(
            "author__name",
            weight="A",
            config="french"
        )
        +
        SearchVector(
            StringAgg("theme__name", Value(" "), default=Value("")),
            weight="B",
            config="french"
        )
        +
        SearchVector(
            StringAgg("tags__name", Value(" "), default=Value("")),
            weight="B",
            config="french"
        )
    )

    # Analyze the search term using the French configuration
    lexemes = [Lexeme(word, prefix=True) for word in search_term.split()] # For prefix search on each word in the search term
    query = SearchQuery(reduce(operator.and_, lexemes), config="french")

    # Search for books matching the query and order them by rank and primary key
    books = (
        Book.objects
        .annotate(
            search=vector,
            rank=SearchRank(vector, query)
        )
        .filter(search=query)
        .order_by("-rank", "pk")
    )

    return books
