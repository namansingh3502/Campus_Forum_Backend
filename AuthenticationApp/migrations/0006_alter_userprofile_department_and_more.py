# Generated by Django 4.0 on 2022-02-02 21:41

import AuthenticationApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum_App', '0006_alter_post_body'),
        ('AuthenticationApp', '0005_alter_userprofile_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='department',
            field=models.CharField(choices=[('', ''), ('CSE', 'CSE'), ('ISE', 'ISE'), ('ECE', 'ECE'), ('EEE', 'EEE'), ('CIVIL', 'CIVIL'), ('MECH', 'MECH')], max_length=5, verbose_name='Department'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('', ''), ('M', 'MALE'), ('F', 'FEMALE')], max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='member_of',
            field=models.ManyToManyField(to='Forum_App.Channel', verbose_name='Channel Member'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=10, verbose_name='Mobile No.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='prefix',
            field=models.CharField(choices=[('', ''), ('Dr.', 'Dr.'), ('Mr.', 'Mr.'), ('Ms.', 'Miss.'), ('Mrs.', 'Mrs.')], max_length=4, verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_image',
            field=models.FileField(upload_to=AuthenticationApp.models.UserProfile.path_and_rename, verbose_name='User Image'),
        ),
    ]
