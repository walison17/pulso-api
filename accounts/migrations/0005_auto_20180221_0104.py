# Generated by Django 2.0 on 2018-02-21 01:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('relationships', '0001_initial'), ('accounts', '0004_auto_20180215_0045')
    ]

    operations = [
        migrations.AddField(
            model_name='user', name='facebook_id', field=models.IntegerField(null=True)
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(
                related_name='followers',
                through='relationships.Follow',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
