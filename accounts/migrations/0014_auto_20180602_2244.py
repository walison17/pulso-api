# Generated by Django 2.0 on 2018-06-02 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='facebook_url',
            field=models.URLField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
    ]
