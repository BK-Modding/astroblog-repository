# Generated by Django 2.0.6 on 2018-06-17 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_profile_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='dismissed',
        ),
    ]
