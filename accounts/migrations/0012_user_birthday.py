# Generated by Django 2.0 on 2018-03-12 21:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0011_remove_user_instagram_url')]

    operations = [
        migrations.AddField(
            model_name='user', name='birthday', field=models.DateTimeField(null=True)
        )
    ]
