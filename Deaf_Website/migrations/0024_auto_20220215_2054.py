# Generated by Django 3.2.3 on 2022-02-15 18:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Deaf_Website', '0023_auto_20220211_1736'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worduser',
            name='vote',
        ),
        migrations.AddField(
            model_name='worduser',
            name='teacher_denied',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='worduser',
            name='vote_approved',
            field=models.ManyToManyField(blank=True, related_name='vote_approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='worduser',
            name='vote_denied',
            field=models.ManyToManyField(blank=True, related_name='vote_denied', to=settings.AUTH_USER_MODEL),
        ),
    ]