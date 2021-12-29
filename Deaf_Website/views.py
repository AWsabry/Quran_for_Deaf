from os import name
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Word
from django.core.paginator import Paginator
from django.core import serializers
import json

# Create your views here.


def index(request):
    return render(request, "index.html")

def words(request):
    words_search = request.GET.get('words_search')
    words = Word.objects.all() if not words_search else Word.objects.filter(name__icontains=words_search)
    page = request.GET.get('page')
    p_obj = Paginator(words, 10)
    p_elibed = p_obj.get_elided_page_range(
        number = p_obj.get_page(page).number,
        on_each_side=1,
        on_ends=1
        )
    
    return render(request, "words.html", {
        'paginator':p_obj.get_page(page),
        'page_elibed': p_elibed
        })
    
def words_ajax(request):
    id = int(request.POST.get('id'))
    word = Word.objects.filter(id=id)
    
    return HttpResponse(serializers.serialize('json' ,word))

def words_search_ajax(request):
    input = request.GET.get('input')
    word = Word.objects.filter(name__icontains=input).values_list('name')
    return HttpResponse(json.dumps(list(dict.fromkeys(word))[:5]))
