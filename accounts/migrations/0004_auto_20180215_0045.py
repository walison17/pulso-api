# Generated by Django 2.0 on 2018-02-15 00:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0003_auto_20180208_1559')]

    operations = [
        migrations.AddField(
            model_name='user', name='facebook_url', field=models.URLField(null=True)
        ),
        migrations.AddField(
            model_name='user', name='instagram_url', field=models.URLField(null=True)
        ),
    ]
