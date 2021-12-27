from os import name
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Word
from django.core.paginator import Paginator
from django.core import serializers

# Create your views here.


def index(request):
    return render(request, "index.html")

def words(request):
    words = Word.objects.all()
    page = request.GET.get('page')
    p_obj = Paginator(words, 1)
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
