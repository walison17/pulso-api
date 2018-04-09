# Generated by Django 2.0 on 2018-04-08 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0004_auto_20180408_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_type',
            field=models.SmallIntegerField(choices=[(0, 'ios'), (1, 'android')], db_index=True, default=1),
        ),
    ]
