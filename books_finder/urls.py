from django.urls import path

from books_finder.views import *

urlpatterns = [
    path('', index, name='index'),
    path('themes/', themes_list, name='themes_list'),
    path('theme/<slug:slug>/', theme_detail, name='theme_detail'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('search/', book_search_view, name='book_search'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('favorites/', favorites, name='favorites'),
]