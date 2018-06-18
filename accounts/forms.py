from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class SignupForm(forms.ModelForm):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    captcha = CaptchaField()

    username.widget.attrs.update({'class': 'white-text', 'name': 'username', 'id': 'username', 'placeholder': 'Enter your username here'})
    email.widget.attrs.update({'placeholder': 'Enter your email here', 'class': 'white-text', 'name': 'email', 'id': 'email'})
    password1.widget.attrs.update({'placeholder': 'Password to register with', 'class': 'white-text', 'name': 'password1', 'id': 'password1'})
    password2.widget.attrs.update(
        {'placeholder': 'Confirm your password here', 'class': 'white-text', 'name': 'password2', 'id': 'password2'})

    captcha.widget.attrs.update({'class': 'white-text', 'placeholder': 'Enter what you see in the image', 'id': 'captcha'})

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email address is already in use.')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        try:
            match = User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError('This username is already in use.')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'captcha')