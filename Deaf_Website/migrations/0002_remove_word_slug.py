# Generated by Django 3.2.3 on 2022-03-10 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Deaf_Website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='slug',
        ),
    ]