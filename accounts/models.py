from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    user_to_notify = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    
    def __str__(self):
        return self.user_to_notify.username + "'s notification: " + self.content[:50]
        
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='images/profiles', blank=True)
    profile_description = models.TextField(default='Another Stargazer!')
    
    def __str__(self):  
        return "%s's profile" % self.user  
        
class Query(models.Model):
    name = models.TextField()
    email = models.EmailField()
    body = models.TextField()
    date_and_time_of_submission = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    moderation_reply = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
        
    def date_and_time_pretty(self):
        return self.date_and_time_of_submission.strftime('%I:%M %p, %b %e, %Y')
