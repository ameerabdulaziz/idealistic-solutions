# Generated by Django 2.1.5 on 2019-01-20 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190119_1943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_type',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='type',
            field=models.CharField(blank=True, choices=[('C', 'Customer'), ('S', 'Staff')], max_length=1, null=True),
        ),
    ]
