from django import template

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