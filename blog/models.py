from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField("self")
    planets = models.IntegerField(default=1)

class Post(models.Model):
    title = models.CharField(max_length=200),
    dateandtime = models.DateTimeField()
    intro = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')
    image = models.ImageField(upload_to='images/')
    totalstars = models.IntegerField(default=1)
    starredby = models.ManyToManyField(User, related_name='starred_by_users')
    keptby = models.ManyToManyField(User, related_name='kept_by_users')
    comments = models.ManyToManyField(Comment, related_name='comments_by_users')