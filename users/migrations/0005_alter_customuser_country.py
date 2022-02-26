# Generated by Django 3.2.3 on 2022-02-26 22:26

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
    ]
