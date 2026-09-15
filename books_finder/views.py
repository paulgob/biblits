from django.shortcuts import render, get_object_or_404
from .models import Theme, Book

def index(request) : 
    themes = Theme.objects.all()     # Récupère tous les thèmes dans la base de donnée
    return render(request, "books_finder/index.html", {"themes": themes})

def theme_detail(request, slug):
    '''
    Display the details of a specific theme and the books associated with it.
    '''
    theme = get_object_or_404(Theme, slug=slug)  # Find the theme by its slug
    books = Book.objects.filter(theme=theme) # Get all books associated with this theme
    return render(request, "books_finder/theme_detail.html", {"theme": theme, "books": books}) 