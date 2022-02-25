from django.urls import path
from . import views

app_name = 'Deaf_Website'

urlpatterns = [
    path("",views.index, name='index'),
    path("words/", views.words, name="words"),
    path("words_ajax/", views.words_ajax, name="words_ajax"),
    path("words_users/", views.words_users, name="words_users"),
    path("words_users_uploads/", views.words_users_uploads, name="words_users_uploads"),
    path("words_search_ajax/", views.words_search_ajax, name="words_search_ajax"),
    path("user_word_vote/", views.user_word_vote, name="user_word_vote"),
    path("pdf/",views.pdf, name='pdf'),
    path("Quran_Platform/", views.Quran_Platform, name="Quran_Platform"),
]