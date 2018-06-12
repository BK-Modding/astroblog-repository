from django.contrib import admin
from .models import Post, Comment, Keep
# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Keep)

class Starredinline(admin.TabularInline):
    model = Post.starredby.through

class StarsAdmin(admin.ModelAdmin):
    inlines = [
        Starredinline,
    ]

class PostAdmin(admin.ModelAdmin):
    inlines = [
        Starredinline,
    ]
    exclude = ('starredby',)

