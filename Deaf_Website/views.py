from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.http import FileResponse
import os
import io
from django.http import HttpResponse, Http404

from Quran_for_Deaf.settings import MEDIA_ROOT

def main(request):
        return render(request,'hello.html')
    
def pdf(request):
    try:
        return FileResponse(open('static/Timeline.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('not found')
    

def video(request):
    
        return render(request,'video.html',{'media': MEDIA_ROOT})
