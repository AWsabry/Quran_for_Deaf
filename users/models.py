from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group, PermissionsMixin, User
from django.utils.timezone import timedelta
from django.utils import timezone
from django_countries.fields import CountryField
from Quran_for_Deaf import settings
from users.utils import AccessTokenGenerator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from Deaf_Website.validators import _ext_photo
# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def get_by_natural_key(self, username):
        """
        To make email login case sensetive.
        """
        
        return self.get(email__iexact=username)

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        
        if not email:
            raise ValueError('Email does not included!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        
        return self.create_user(email=email, password=password, first_name=first_name, last_name=last_name, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email address', unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    country = CountryField(blank_label=_('(select country)'), null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    Age = models.CharField(max_length=10, default='', null=True, blank=True)
    PhoneNumber = models.CharField(max_length=20, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    ProfilePic = models.ImageField(upload_to="TeacherProfile/", null=True, blank=True, validators=[_ext_photo])
    Experience = models.TextField(blank=True, null=True)
    CV = models.FileField(upload_to="TeacherProfile/TeacherCV", null=True, blank=True)
    
    # 3 Boolean Questions with conditions
    question_one = models.BooleanField(verbose_name=_('Are you Deaf?'),default=False)
    question_two = models.BooleanField(verbose_name=_('Are you specialized in dealing with deaf people?'),default=False)
    question_three = models.BooleanField(verbose_name=_('Do you have one from your family who are deaf?'),default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

class AccessToken(models.Model):
    token = models.CharField(max_length=500, blank=True)
    user = models.ForeignKey(to= CustomUser, on_delete=models.CASCADE, related_name='token')
    expires = models.DateTimeField()
    created = models.DateTimeField(auto_now=True, editable=False)
    
    def __str__(self):
        return self.token
    
    class Meta:
        ordering = ('-created',)

@receiver(pre_save, sender=AccessToken)
def token_save(sender, instance, **kwargs):
    instance.token = AccessTokenGenerator().make_token(instance.user)
    instance.expires = timezone.now() + timedelta(seconds=settings.AUTH_EMAIL_ACTIVATE_EXPIRE)
    
@receiver(post_save, sender=CustomUser)
def teacher_group(sender, instance, **kwargs):
    group = Group.objects.filter(name='Teachers').first()
    
    if group and instance.is_teacher:
        group.user_set.add(instance)
    else:
        group.user_set.remove(instance)    
