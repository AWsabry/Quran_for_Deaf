from ast import arg
from django.db.models import Q
from numpy import require
from users.models import CustomUser
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.forms import ValidationError
from Deaf_Website.validators import _ext_photo, _ext_video
import re
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadFiles(object):

    def __init__(self, model, file_type):
        self.model = model
        self.file_type = file_type
        

    def __call__(self, instance, filename):
        return 'users/%s/%s/%s/%s' % (instance.user.email, self.model, self.file_type, filename)

class Word(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(unique=True, db_index=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=UploadFiles('Words', 'photo'), blank=True, validators=[_ext_photo], null=True)
    video = models.FileField(upload_to=UploadFiles('Words', 'video'), blank=True, validators=[_ext_video], null=True)
    active = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    word_attach = models.OneToOneField('Word', on_delete=models.CASCADE, null=True)
    user_agree = models.ManyToManyField(CustomUser, related_name='user_agree',blank=True)
    user_disagree = models.ManyToManyField(CustomUser, related_name='user_disagree', blank=True)
    
    user_agree_count = models.PositiveIntegerField(default=0)
    user_disagree_count = models.PositiveIntegerField(default=0)

    def slug_make(self):
        value = re.sub(r'[^\w\s-]', '', f'{self.name.lower()}-{self.id}')
        return re.sub(r'[-\s]+', '-', value).encode('utf-8').decode().strip('-_')
    
    def clean(self):
        if not (self.video or self.image):
            raise ValidationError('Please add video or photo') 
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}-{self.id}'


class WordUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    word = models.OneToOneField(Word, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=UploadFiles('WordUser', 'photo'), blank=True, validators=[_ext_photo], null=True)
    video = models.FileField(upload_to=UploadFiles('WordUser', 'video'), blank=True, validators=[_ext_video], null=True)
    vote_denied = models.ManyToManyField(to=CustomUser, related_name='vote_denied_relate', blank=True)
    vote_approved = models.ManyToManyField(to=CustomUser, related_name='vote_approved_relate', blank=True)
    vote_nothing = models.ManyToManyField(to=CustomUser, related_name='vote_nothing_relate', blank=True)
    vote_teacher = models.BooleanField(blank=False, null=True)
    vote_percentage = models.CharField(max_length=100, blank=True)
    teacher_approved = models.IntegerField(null=True)
    teacher_denied = models.IntegerField(null=True)
    teacher_num = models.IntegerField(null=True)

    def clean(self):
        if not (self.video or self.image):
            raise ValidationError('Please add video or photo') 
    
    def __str__(self):
        return self.word.user.email

@receiver(post_save, sender=Word)
def word_postsave(sender, instance, created, **kwargs):
    update_fields = kwargs['update_fields']
    obj = sender.objects.filter(id=instance.id)
    obj.update(slug=obj[0].slug_make())

@receiver(m2m_changed, sender=WordUser.vote_approved.through)
def approved_pre_add(sender, instance, action, **kwargs):
    if action == 'pre_add':
        print(f'approved_pre - {action}')
        pk_set = CustomUser.objects.filter(id__in=kwargs['pk_set'])
        intersection = instance.vote_denied.all().intersection(pk_set)
        print(pk_set)
        if intersection:
            print('removed_vote_denied')
            instance.vote_denied.remove(*intersection)
            
    if action == 'post_remove' or action == 'post_add':

        teachers = CustomUser.objects.filter(Q(is_teacher=True, is_active=True) | Q(is_superuser=True))
        teachers_votes = instance.vote_approved.all() #approved
        
        # This will approve the post
        if not teachers.difference(teachers_votes).count():
            new_obj = Word.objects.create(user=instance.user,
                                word_attach=instance.word,
                                name=instance.word.name,
                                description=instance.word.description,
                                image=instance.image,
                                video=instance.video,
                                active=True)
            instance.delete()

@receiver(m2m_changed, sender=WordUser.vote_denied.through)
def denied_pre_add(sender, instance, action, **kwargs):
    if action == 'pre_add':
        print(f'denied_pre - {action}')
        print(kwargs)
        pk_set = CustomUser.objects.filter(id__in=kwargs['pk_set'])
        print(pk_set)
        intersection = instance.vote_approved.all().intersection(pk_set)
        if intersection:
            print('removed_vote_approved')
            instance.vote_approved.remove(*intersection)