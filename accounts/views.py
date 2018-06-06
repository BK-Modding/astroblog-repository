from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Notification

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'GET':
            return render(request, 'accounts/authenticate.html')
        elif request.method == 'POST':
            if request.POST['username'] and request.POST['password'] and request.POST['confirmpassword'] and request.POST['email']:
                if request.POST['password'] == request.POST['confirmpassword']:
                    username_flag = 0
                    email_flag = 0
                    try:
                        username_users = User.objects.get(username=request.POST['username'])
                        username_flag = 1
                        return render(request, 'accounts/authenticate.html', {'signup_error': 'That username already exists'})
                    except User.DoesNotExist:
                        pass
                    try:
                        email_users = User.objects.get(email=request.POST['email'])
                        email_flag = 1
                        return render(request, 'accounts/authenticate.html', {'signup_error': 'That email already exists'})
                    except User.DoesNotExist:
                        pass
                    
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'])
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'accounts/authenticate.html', {'signup_error': 'The passwords do not match'})
            else:
                return render(request, 'accounts/authenticate.html', {'signup_error': 'Error, some fields are not filled'})
def login(request):
    if request.user.is_authenticated:
         return redirect('index')
    else:
        if request.method == 'GET':
            return render(request, 'accounts/authenticate.html')
        elif request.method == 'POST':
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                return redirect('index')
            else:
                return render(request, 'accounts/authenticate.html', {'login_error': 'Invalid credentials'})
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

@login_required()
def notifications(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    notify_objs = Notification.objects.filter(user_to_notify=user)
    
    return render(request, 'accounts/notifications.html', {'notifications': notify_objs})