from django.urls import path

from books_finder.views import *

urlpatterns = [
    path('', index, name='index'),
    path('theme/<slug:slug>/', theme_detail, name='theme_detail'),
]