from django import template

from Deaf_Website.models import Word, WordUser
from django.db.models import Q

register = template.Library()

@register.filter
def convert_to_eastern_arabic(value):
    arabic_num = ''
    for c in str(value):
        if 0 <= int(c) < 10:
            eastern_arabic_number = r"\u066%s" % c
            arabic_num += eastern_arabic_number
    return arabic_num.encode().decode('unicode_escape')

@register.filter
def get_url(page, words_search):
    if words_search:
        return f'?words_search={words_search}&page={page}'
    
    return f'?page={page}'

@register.filter
def word_user_check(user, word):
    check = True if WordUser.objects.filter(user=user, word=word) else False
    return check

@register.filter
def word_check(user, word):
    print(user)
    print(word.slug)
    check = True if Word.objects.filter(user=user, word_attach=word) else False
    
    print(check)
    return check

@register.filter
def word_user_vote_check(user, word):
    check = False
    
    if Word.objects.filter(id=word, user_agree=user):
        check = 'agree'
        
    if Word.objects.filter(id=word ,user_disagree=user):
        check = 'disagree'
    
    return check