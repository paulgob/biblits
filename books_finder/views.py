from django.shortcuts import render, get_object_or_404
from .services import search_books
from .models import Theme, Book

def index(request) : 
    themes = Theme.objects.all()
    return render(request, "books_finder/index.html", {"themes": themes})

def theme_detail(request, slug):
    '''
    Display the details of a specific theme and the books associated with it.
    '''
    theme = get_object_or_404(Theme, slug=slug)  # Find the theme by its slug
    books = Book.objects.filter(theme=theme) # Get all books associated with this theme
    return render(request, "books_finder/theme_detail.html", {"theme": theme, "books": books}) 

def book_detail(request, pk):
    '''
    Display the details of a specific book.
    '''
    book = get_object_or_404(Book, pk=pk)  # Find the book by its primary key
    return render(request, "books_finder/book_detail.html", {"book": book})

def book_search_view(request):
    '''
    Handle the search functionality for books.
    '''
    search_term = request.GET.get("q", "").strip()

    books = search_books(search_term)

    context = {
        "books": books,
        "search_term": search_term,
    }

    return render(
        request,
        "books_finder/index.html",
        context
    )