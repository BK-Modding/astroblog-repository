from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def signup(request):
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
    if request.method == 'GET':
        return render(request, 'accounts/authenticate.html')
    
def logout(request):
    #TODO
    pass