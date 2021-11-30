from django.conf import settings
from django.db import models

# Create your models here.


class TeacherProfile(models.Model):
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    slug = models.SlugField(unique=True, db_index=True, default='teacher')
    FirstName = models.CharField(max_length=50, default='', null=True)
    LastName = models.CharField(max_length=50, default='', null=True)
    Age = models.CharField(max_length=10, default='', null=True)
    PhoneNumber = models.IntegerField()
    last_modified = models.DateTimeField(auto_now=True)
    ProfilePic = models.ImageField(upload_to="TeacherProfile/", null=True)
    IdentityID = models.IntegerField()
    Experience = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    CV = models.FileField(upload_to="TeacherProfile/TeacherCV", null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.FirstName} ({self.LastName})"


class Category(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    image = models.ImageField(upload_to="categories", blank=True)
    brand = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class UploadedVideo(models.Model):
    name = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(unique=True, db_index=True)
    video = models.FileField(upload_to="Deaf_Signs", blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    counter = models.IntegerField(default=0, null=True)
    PositiveFeedBack = models.IntegerField(default=0, null=True)
    NegativeFeedBack = models.IntegerField(default=0, null=True)

    class Meta:
        verbose_name_plural = "UploadedVideos"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"
