# Generated by Django 2.0.6 on 2018-06-08 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_remove_post_keptby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keep',
            old_name='blogpost',
            new_name='blog_post',
        ),
    ]
