# Generated by Django 2.0 on 2018-03-09 00:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('pulsos', '0002_auto_20180306_0044')]

    operations = [
        migrations.AddField(
            model_name='pulso',
            name='is_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pulso',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]
