from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField("self", blank=True)
    comment_date_and_time = models.DateTimeField()
    planets = models.PositiveIntegerField(default=1)
    planetedby = models.ManyToManyField(User, related_name='planeted_by_users')
    
    def __str__(self):
        return self.commenter.username + ': ' + self.comment[:50] + '...'

class Post(models.Model):
    title = models.CharField(max_length=200)
    dateandtime = models.DateTimeField() # auto
    intro = models.CharField(max_length=200)
    CATEGORY_CHOICES = (
        ('Stars and Planets', 'Stars and Planets'),
        ('Neutron stars and Pulsars', 'Neutron stars and Pulsars'),
        ('Black holes and Quasars', 'Black holes and Quasars'),
        ('Galaxies and Cosmology', 'Galaxies and Cosmology'),
        ('Relativity in Astro', 'Relativity in Astro'),
        ('Particle Physics and Quantum Mechanics in Astro', 'Particle Physics and Quantum Mechanics in Astro'),
        ('String Theory in Astro', 'String Theory in Astro'),
        ('Astronomy', 'Astronomy'),
        ('Scientific Literature', 'Scientific Literature')
    )
    category = models.TextField(
        choices=CATEGORY_CHOICES,
        default='Stars and Planets'
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user') # auto
    image = models.ImageField(upload_to='images/')
    body = HTMLField()
    totalstars = models.PositiveIntegerField(default=1)
    starredby = models.ManyToManyField(User, related_name='starred_by_users', blank=True)
    totalkeeps = models.PositiveIntegerField(default=1)
    comments = models.ManyToManyField(Comment, related_name='comments_by_users', blank=True)
    is_approved = models.BooleanField(default=False)
    is_denied = models.BooleanField(default=False)
    moderation_comments = models.TextField(default='', blank=True)
    
    
    def __str__(self):
        return self.title
        
    def summary(self):
        return self.body[:300]

    def dateandtimepretty(self):
        return custom_strftime('%B {S}, %Y', self.dateandtime)
        
class Keep(models.Model):
    blog_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    keep_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
    
    def __str__(self):
        return self.keep_user.username + "'s keep: " + self.blog_post.title

