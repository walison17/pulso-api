# Generated by Django 2.0 on 2018-02-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('accounts', '0002_auto_20180207_0051')]

    operations = [
        migrations.RemoveField(model_name='user', name='photo'),
        migrations.AddField(
            model_name='user',
            name='photo_url',
            field=models.URLField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
