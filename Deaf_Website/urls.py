from django.urls import path
from . import views

<<<<<<< HEAD
=======
app_name = 'Deaf_Website'

>>>>>>> origin/master
urlpatterns = [
    path("",views.index, name='index'),
    path("words/", views.words, name="words"),
    path("words_ajax/", views.words_ajax, name="words_ajax"),
    path("words_search_ajax/", views.words_search_ajax, name="words_search_ajax"),
<<<<<<< HEAD
=======
    path("pdf/",views.pdf, name='pdf'),
    path("Quran_Platform/", views.Quran_Platform, name="Quran_Platform"),
>>>>>>> origin/master
]