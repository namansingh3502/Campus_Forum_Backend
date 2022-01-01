# Generated by Django 4.0 on 2022-01-01 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum_App', '0001_initial'),
        ('AuthenticationApp', '0003_remove_userprofile_member_userprofile_member_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='member_of',
            field=models.ManyToManyField(blank=True, to='Forum_App.Channel', verbose_name='Channel Member'),
        ),
    ]
