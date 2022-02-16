from tabnanny import check
from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Word, WordUser
from django.core.paginator import Paginator
from django.core import serializers
import json
from Quran_for_Deaf import settings

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
        'page_elibed': p_elibed,
        'word':words[0]
        })
    
def words_ajax(request):
    id = int(request.POST.get('id'))
    word = Word.objects.filter(id=id)

    return HttpResponse(serializers.serialize('json' ,word))

def words_users(request):
    input = json.loads(request.POST.get('input'))
    input_image = input.get('image')
    input_video = input.get('video')
    
    if input_image:
        size = input_image.get('size')
        ext = input_image.get('ext')
        
        # clear data
        input['image'].clear()
        
        if int(size) <= settings.MAXIMUM_SIZE_ALLOWED_PHOTO:
            input['image'].update({'size':True})
        else:
            input['image'].update({'size':False})
        
        extension = ext.split('/')[1] if 'image' in ext else None
        if f'.{extension}' in settings.ALLOWED_EXT_PHOTO:
            input['image'].update({'ext':True})
        else:
            input['image'].update({'ext':False})

        input['image'].update({'conditions':{'size':(settings.MAXIMUM_SIZE_ALLOWED_PHOTO/1024/1024), 'ext':settings.ALLOWED_EXT_PHOTO}})
    else:
        input['image'] = 0
        
    if input_video:
        size = input_video.get('size')
        ext = input_video.get('ext')
        
        # clear data
        input['video'].clear()
        
        if int(size) <= settings.MAXIMUM_SIZE_ALLOWED_VIDEO:
            input['video'].update({'size':True})
        else:
            input['video'].update({'size':False})
        
        extension = ext.split('/')[1] if 'video' in ext else None
        if f'.{extension}' in settings.ALLOWED_EXT_VIDEO:
            input['video'].update({'ext':True})
        else:
            input['video'].update({'ext':False})

        input['video'].update({'conditions':{'size':(settings.MAXIMUM_SIZE_ALLOWED_VIDEO/1024/1024), 'ext':settings.ALLOWED_EXT_VIDEO}})
    else:
        input['video'] = 0
    
    return HttpResponse(json.dumps(input))

def words_users_uploads(request):
    print(request.headers)
    print('#'*50)
    print(request.POST)
    print(request.FILES)
    
    return HttpResponse('hesham')

def words_search_ajax(request):
    input = request.GET.get('input')
    word = Word.objects.filter(name__icontains=input).values_list('name')
    return HttpResponse(json.dumps(list(dict.fromkeys(word))[:5]))


def pdf(request):
    return render(request, "pdf.html")


def Quran_Platform(request):
    return render(request,'Quran_Platform.html')
