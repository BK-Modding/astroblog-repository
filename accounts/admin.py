from django.contrib import admin
from .models import Notification, Query, UserProfile

# Register your models here.
admin.site.register(Notification)
admin.site.register(Query)
admin.site.register(UserProfile)
