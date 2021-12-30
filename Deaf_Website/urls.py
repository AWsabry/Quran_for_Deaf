from django.urls import path
from . import views

app_name = 'Deaf_Website'

urlpatterns = [
    path("",views.index, name='index'),
    path("words/", views.words, name="words"),
    path("words_ajax/", views.words_ajax, name="words_ajax"),
    path("words_search_ajax/", views.words_search_ajax, name="words_search_ajax"),
    path("pdf/",views.pdf, name='pdf'),
    path("Quran_Platform/", views.Quran_Platform, name="Quran_Platform"),
]