# Generated by Django 2.0 on 2018-03-09 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20180221_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='instagram_url',
        ),
    ]
