from django.shortcuts import render
import json
# Create your views here.


def index(request):
    return render(request, "index.html")

def words(request):
    return render(request, "words.html")
