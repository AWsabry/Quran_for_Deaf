# Generated by Django 3.2.3 on 2022-02-11 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deaf_Website', '0012_alter_worduser_vote_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worduser',
            name='vote_teacher',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
