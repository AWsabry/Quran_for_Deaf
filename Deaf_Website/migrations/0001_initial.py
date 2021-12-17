# Generated by Django 3.2.3 on 2021-12-13 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(blank=True, upload_to='categories')),
                ('brand', models.CharField(blank=True, max_length=250)),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(default='teacher', unique=True)),
                ('FirstName', models.CharField(default='', max_length=50, null=True)),
                ('LastName', models.CharField(default='', max_length=50, null=True)),
                ('Age', models.CharField(default='', max_length=10, null=True)),
                ('PhoneNumber', models.IntegerField()),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('ProfilePic', models.ImageField(null=True, upload_to='TeacherProfile/')),
                ('IdentityID', models.IntegerField()),
                ('Experience', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('CV', models.FileField(null=True, upload_to='TeacherProfile/TeacherCV')),
            ],
        ),
        migrations.CreateModel(
            name='UploadedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('slug', models.SlugField(unique=True)),
                ('video', models.FileField(blank=True, upload_to='Deaf_Signs')),
                ('description', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('counter', models.IntegerField(default=0, null=True)),
                ('PositiveFeedBack', models.IntegerField(default=0, null=True)),
                ('NegativeFeedBack', models.IntegerField(default=0, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Deaf_Website.category')),
            ],
            options={
                'verbose_name_plural': 'UploadedVideos',
            },
        ),
    ]
