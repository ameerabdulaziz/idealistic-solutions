# Generated by Django 2.1.5 on 2019-01-19 23:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing_system', '0002_auto_20190111_2333'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ('created_at',)},
        ),
    ]