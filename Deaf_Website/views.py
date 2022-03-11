from tabnanny import check
from django.http.response import HttpResponse
from django.shortcuts import render
from numpy import imag
from .models import Word, WordUser
from users.models import CustomUser
from django.core.paginator import Paginator
from django.core import serializers
import json
from Quran_for_Deaf import settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib import messages
from difflib import SequenceMatcher
# Create your views here.

def index(request):
    return render(request, "index.html")

def words(request):
    words_search = request.GET.get('words_search')
    user = CustomUser.objects.annotate(full_name=Concat('first_name',Value(' '), 'last_name')).filter(full_name__icontains=words_search) if words_search else None
    
    words = Word.objects.filter(name__icontains=words_search) if words_search else None
    user_words = Word.objects.filter(user__in=user) if words_search else None
    
    if user and user_words:
        words = Word.objects.filter(user__in=user)
        messages.success(request, f'عدد نتائج البحث عن كلمة {words_search} هو "{words.count()}" نتيجة', extra_tags='searching')
    elif user and not user_words:
        words = Word.objects.all()
        if Word.objects.filter(name__icontains=words_search):
            words = Word.objects.filter(name__icontains=words_search)
            messages.success(request, f'عدد نتائج البحث عن كلمة {words_search} هو "{words.count()}" نتيجة', extra_tags='searching')
        else:
            messages.success(request, f'لا يوجد منشورات لـ {user[0].first_name} {user[0].last_name}', extra_tags='searching')
    elif words:
        messages.success(request, f'عدد نتائج البحث عن كلمة {words_search} هو "{words.count()}" نتيجة', extra_tags='searching')
    else:
        if hasattr(words, 'count'):
            messages.success(request, f'لا توجد نتائج لـ {words_search} التي تبحث عنها', extra_tags='searching')
        words = Word.objects.all()
    
    page = request.GET.get('page')
    p_obj = Paginator(words.order_by('user__is_teacher'), 10)
    p_elibed = p_obj.get_elided_page_range(
        number = p_obj.get_page(page).number,
        on_each_side=1,
        on_ends=1
        )
    return render(request, "words.html", {
        'paginator':p_obj.get_page(page),
        'page_elibed': p_elibed,
        'word':words[0],
        'word_all':Word.objects.all().count()
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

@ensure_csrf_cookie
def words_users_uploads(request):
    word = Word.objects.filter(id=int(request.POST.get('word')))[0]
    image = request.FILES.get('image')
    video = request.FILES.get('video')

    if image or video:
        if not WordUser.objects.filter(user=request.user, word=word):
            WordUser.objects.create(user=request.user,
                                    word=word,
                                    image=image,
                                    video=video)
        
    return HttpResponse(word.name)

def words_search_ajax(request):
    input = request.GET.get('input')
    user = CustomUser.objects.annotate(
        full_name=Concat('first_name',Value(' '), 'last_name')
    ).filter(is_active=True).distinct().values_list('full_name')
    
    user = sorted(user, key=lambda x: SequenceMatcher(lambda x: x == ' ', input, x[0]).ratio(), reverse=True)[:3]

    word = Word.objects.all().distinct().values_list('name')
    word = sorted(word, key=lambda x: SequenceMatcher(None, input, x[0]).ratio(), reverse=True)[:5]
    
    return HttpResponse(json.dumps({'user':user,'word':word}))

@csrf_exempt
def user_word_vote(request):
    word = request.POST.get('word')
    vote = request.POST.get('vote')
    print(vote)
    print(Word.objects.filter(Q(id=int(word)) & (~Q(user_agree=request.user) & ~Q(user_disagree=request.user))))
    if Word.objects.filter(Q(id=int(word)) & (~Q(user_agree=request.user) & ~Q(user_disagree=request.user))):
        if vote == 'agree':
            Word.objects.filter(id=int(word))[0].user_agree.add(request.user)
            
            return HttpResponse('agree')
        elif vote == 'disagree':
            Word.objects.filter(id=int(word))[0].user_disagree.add(request.user)
            return HttpResponse('disagree')
    
    return HttpResponse('No')

def pdf(request):
    return render(request, "pdf.html")


def Quran_Platform(request):
    return render(request,'Quran_Platform.html')
