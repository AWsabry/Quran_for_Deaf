# Generated by Django 3.2.3 on 2021-12-29 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='Age',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='CV',
            field=models.FileField(null=True, upload_to='TeacherProfile/TeacherCV'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='Experience',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='PhoneNumber',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='ProfilePic',
            field=models.ImageField(null=True, upload_to='TeacherProfile/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
