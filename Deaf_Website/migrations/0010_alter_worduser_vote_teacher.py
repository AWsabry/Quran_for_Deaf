# Generated by Django 3.2.3 on 2022-02-11 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Deaf_Website', '0009_alter_worduser_vote_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worduser',
            name='vote_teacher',
            field=models.CharField(choices=[('None', None), ('Yes', True), ('No', False)], max_length=100, null=True),
        ),
    ]
