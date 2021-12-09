from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path("video",views.video),
    path('', views.main, name = 'main'), url(r'^pdf', views.pdf, name = 'pdf'), 
]