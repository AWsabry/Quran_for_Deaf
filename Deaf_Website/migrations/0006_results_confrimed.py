# Generated by Django 3.2.3 on 2021-12-04 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deaf_Website', '0005_auto_20211204_2032'),
    ]

    operations = [
        migrations.AddField(
            model_name='results',
            name='Confrimed',
            field=models.BooleanField(default=False),
        ),
    ]