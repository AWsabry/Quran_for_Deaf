# Generated by Django 3.2.3 on 2022-02-11 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deaf_Website', '0014_alter_worduser_vote_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worduser',
            name='vote_teacher',
            field=models.BooleanField(choices=[(True, 'نعم'), (False, 'لا')], default=None, null=True),
        ),
    ]
