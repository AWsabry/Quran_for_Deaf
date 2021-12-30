# Generated by Django 3.2.3 on 2021-12-27 21:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Deaf_Website', '0006_auto_20211227_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='worduser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
