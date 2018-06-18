from django import forms
from tinymce import TinyMCE
from .models import Post
from django.utils import timezone


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['dateandtime', 'author', 'totalstars', 'totalkeeps', 'starredby', 'keptby', 'comments']
