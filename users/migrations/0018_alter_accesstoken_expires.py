# Generated by Django 3.2.3 on 2021-12-07 14:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_accesstoken_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 7, 14, 42, 11, 288067, tzinfo=utc)),
        ),
    ]
