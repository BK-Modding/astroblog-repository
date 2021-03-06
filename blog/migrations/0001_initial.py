# Generated by Django 2.0.6 on 2018-06-05 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('planets', models.IntegerField(default=1)),
                ('commenter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comments', models.ManyToManyField(related_name='_comment_comments_+', to='blog.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateandtime', models.DateTimeField()),
                ('intro', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('totalstars', models.IntegerField(default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_user', to=settings.AUTH_USER_MODEL)),
                ('keptby', models.ManyToManyField(related_name='kept_by_users', to=settings.AUTH_USER_MODEL)),
                ('starredby', models.ManyToManyField(related_name='starred_by_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
