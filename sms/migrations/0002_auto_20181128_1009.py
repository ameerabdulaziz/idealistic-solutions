# Generated by Django 2.1.1 on 2018-11-28 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonebook',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='smsgeteway',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='template',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
