from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Notification, UserProfile
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password


def get_notify_count(user):
    usernotifications = None
    if user.is_authenticated:
        usernotifications = Notification.objects.filter(user_to_notify=user, dismissed=False).count()

    return usernotifications


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'GET':
            return render(request, 'accounts/authenticate.html')
        elif request.method == 'POST':
            if request.POST['username'] and request.POST['password'] and request.POST['confirmpassword'] and \
                    request.POST['email']:
                if request.POST['password'] == request.POST['confirmpassword']:
                    username_flag = 0
                    email_flag = 0
                    try:
                        username_users = User.objects.get(username=request.POST['username'])
                        username_flag = 1
                        return render(request, 'accounts/authenticate.html',
                                      {'signup_error': 'That username already exists'})
                    except User.DoesNotExist:
                        pass
                    try:
                        email_users = User.objects.get(email=request.POST['email'])
                        email_flag = 1
                        return render(request, 'accounts/authenticate.html',
                                      {'signup_error': 'That email already exists'})
                    except User.DoesNotExist:
                        pass

                    user = User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['password'], email=request.POST['email'])
                    user_profile = UserProfile()
                    user_profile.user = user
                    user_profile.save()
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'accounts/authenticate.html', {'signup_error': 'The passwords do not match'})
            else:
                return render(request, 'accounts/authenticate.html',
                              {'signup_error': 'Error, some fields are not filled'})


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
                if request.POST.get('next'):
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return redirect('index')
            else:
                return render(request, 'accounts/authenticate.html', {'login_error': 'Invalid credentials'})


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')


@login_required
def changepassword(request, user_id):
    if request.method == 'POST':
        if request.user.id == user_id:
            if request.POST['oldpassword'] and request.POST['newpassword'] and request.POST['confirmnewpassword']:
                if request.user.check_password(request.POST['oldpassword']):
                    if request.POST['newpassword'] == request.POST['confirmnewpassword']:
                        user = get_object_or_404(User, pk=user_id)
                        user.set_password(request.POST['newpassword'])
                        user.save()
                        return render(request, 'accounts/changepassword.html',
                                      {'change_password_success': 'Password changed successfully',
                                       'notification_count': get_notify_count(request.user)})
                    else:
                        return render(request, 'accounts/changepassword.html',
                                      {
                                          'change_password_error': 'Error, the new password and the confirmation password do not match',
                                          'notification_count': get_notify_count(request.user)})
                else:
                    return render(request, 'accounts/changepassword.html',
                                  {'change_password_error': 'Error, the existing password entered is incorrect',
                                   'notification_count': get_notify_count(request.user)})
            else:
                return render(request, 'accounts/changepassword.html',
                              {'change_password_error': 'Error, some fields have not been filled',
                               'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
    elif request.method == 'GET':
        return render(request, 'accounts/changepassword.html',
                      {'notification_count': get_notify_count(request.user)})


@login_required()
def notifications(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        notify_objs = Notification.objects.filter(user_to_notify=request.user, dismissed=False)

        return render(request, 'accounts/notifications.html',
                      {'notifications': notify_objs, 'notification_count': get_notify_count(request.user)})
    else:
        return redirect('unauthorized')


@login_required
def dismiss_notification(request, user_id, notify_id):
    if request.method == 'POST':
        if request.user.id == user_id:
            notification = get_object_or_404(Notification, pk=notify_id)
            notification.dismissed = True
            notification.save()
            notifications = Notification.objects.filter(user_to_notify=request.user, dismissed=False)
            return render(request, 'accounts/notifications.html',
                          {'notifications': notifications, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
