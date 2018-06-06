from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notification(models.Model):
    user_to_notify = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    
    
    def __str__(self):
        return self.user_to_notify.username + "'s notification"
