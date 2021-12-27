from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name='index'),
    path("words/", views.words, name="words"),
    path("words_ajax/", views.words_ajax, name="words_ajax")
]