"""
URL configuration for biblits project.
"""
from django.contrib import admin
from django.urls import include, path

from books_finder.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books_finder.urls')),  # Include the URLs from the books_finder app
]
