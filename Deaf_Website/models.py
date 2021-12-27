from functools import wraps
from os import name
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from Deaf_Website.validators import _ext_photo, _ext_video
import re

# Create your models here.

def upload_files(model, file_type):
    def wrapper(instance, filename):
        name = instance.name if 'name' in instance.__dict__ else instance.word.name
        return u'users/%s/%s/%s/%s/%s' % (instance.user.email, model, name, file_type, filename)
    return wrapper

class Word(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(unique=True, db_index=True, allow_unicode=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=upload_files('Words', 'photo'), blank=True, validators=[_ext_photo], null=True)
    video = models.FileField(upload_to=upload_files('Words', 'video'), blank=True, validators=[_ext_video], null=True)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def slug_make(self):
        value = re.sub(r'[^\w\s-]', '', f'{self.name.lower()}-{self.id}')
        return re.sub(r'[-\s]+', '-', value).strip('-_')
    
    def clean(self):
        if not (self.video or self.image):
            raise ValidationError('Please add video or photo') 
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.slug
        

class WordUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_files('WordUser', 'photo'), blank=True, validators=[_ext_photo], null=True)
    video = models.FileField(upload_to=upload_files('WordUser', 'video'), blank=True, validators=[_ext_video], null=True)

    def clean(self):
        if not (self.video or self.image):
            raise ValidationError('Please add video or photo') 

    def __str__(self):
        return self.word.user.email


@receiver(post_save, sender=Word)
def word_presave(sender, instance, created, **kwargs):
    obj = sender.objects.filter(id=instance.id)
    obj.update(slug=obj[0].slug_make())
    
@receiver(post_save, sender=WordUser)
def word_presave(sender, instance, created, **kwargs):
    if created:
        neWord = Word.objects.create(user=instance.user, name=instance.word.name, slug=f'{instance.word.slug}-2', description=instance.word.description)
        