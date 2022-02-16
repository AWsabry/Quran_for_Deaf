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

# def upload_files(model, file_type):
#     def wrapper(instance, filename):
#         return 'users/%s/%s/%s/%s' % (instance.user.email, model, file_type, filename)
#     return wrapper

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

    def slug_make(self):
        value = re.sub(r'[^\w\s-]', '', f'{self.name.lower()}-{self.id}')
        return re.sub(r'[-\s]+', '-', value).encode('utf-8').decode().strip('-_')
    
    def clean(self):
        if not (self.video or self.image):
            raise ValidationError('Please add video or photo') 
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class WordUser(models.Model):
    choices = (
        (None, 'لم يتم الإختيار'),
        (True, 'نعم'),
        (False, 'لا'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True)
    word = models.OneToOneField(Word, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to=UploadFiles('WordUser', 'photo'), blank=True, validators=[_ext_photo], null=True)
    video = models.FileField(upload_to=UploadFiles('WordUser', 'video'), blank=True, validators=[_ext_video], null=True)
    vote_approved = models.ManyToManyField(to=CustomUser, related_name='vote_approved', blank=True)
    vote_denied = models.ManyToManyField(to=CustomUser, related_name='vote_denied', blank=True)
    vote_teacher = models.BooleanField(default=None, choices=choices, null=True)
    vote_percentage = models.CharField(max_length=100, blank=True)
    teacher_approved = models.IntegerField(null=True)
    teacher_denied = models.IntegerField(null=True)
    teacher_num = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
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
    if action == 'post_add':
        print('#####m2m_changed######')
        print(instance.vote_approved.all())
        raise ValidationError('ؤاثؤن')

@receiver(m2m_changed, sender=WordUser.vote_approved.through)
def approved_post_add(sender, instance, action, **kwargs):
    if action == 'post_remove' or action == 'post_add':

        teachers = CustomUser.objects.filter(Q(is_teacher=True) | Q(is_superuser=True))
        teachers_votes = instance.vote_approved.all() #approved
        
        # This will approve the post
        if not teachers.difference(teachers_votes).count():
            new_obj = Word.objects.create(user=instance.user,
                                name=instance.word.name,
                                description=instance.word.description,
                                image=instance.image,
                                video=instance.video,
                                active=True)
            instance.delete()
        else:
            percentage = (teachers_votes.count()/teachers.count())*100 #teachers.difference(teachers_votes).count()
            instance.vote_percentage = f'{round(percentage,1)} %'
            instance.save()

