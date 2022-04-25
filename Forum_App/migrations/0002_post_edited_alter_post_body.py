# Generated by Django 4.0.3 on 2022-04-25 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forum_App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True, verbose_name='Post text'),
        ),
    ]