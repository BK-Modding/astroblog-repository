# Generated by Django 2.0.6 on 2018-06-06 00:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20180605_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments_by_users', to='blog.Comment'),
        ),
        migrations.AlterField(
            model_name='post',
            name='keptby',
            field=models.ManyToManyField(blank=True, related_name='kept_by_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='moderation_comments',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='starredby',
            field=models.ManyToManyField(blank=True, related_name='starred_by_users', to=settings.AUTH_USER_MODEL),
        ),
    ]