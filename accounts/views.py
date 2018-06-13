from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import Notification, UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
try:
    from astroblog import local_settings
except ImportError:
    print("import error")
    pass


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
                    user.is_active = False
                    user.save()
                    user_profile = UserProfile()
                    user_profile.user = user
                    user_profile.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your Astroblog account.'
                    message = render_to_string('accounts/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = request.POST['email']
                    from_email = local_settings.DEFAULT_FROM_EMAIL
                    recipient_list = [to_email, 'kavesbteja@gmail.com']
                    send_mail(mail_subject, '', from_email, recipient_list, fail_silently=False,
                              html_message=message)

                    return render(request, 'accounts/authenticate.html', {'signup_success': 'Your account has been successfully created, please verify it as an email has been sent to the registered email address'})
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
                if user.is_active:
                    auth.login(request, user)
                    if request.POST.get('next'):
                        return HttpResponseRedirect(request.POST.get('next'))
                    else:
                        return redirect('index')
                else:
                    return render(request, 'accounts/authenticate.html', {'login_error': 'This account has not yet been verified, please verify it before logging in'})
            else:
                return render(request, 'accounts/authenticate.html', {'login_error': 'Invalid credentials or this account has not yet been verified, please verify it before logging in'})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index')

@login_required()
def notifications(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        notify_objs = Notification.objects.filter(user_to_notify=request.user, dismissed=False)
        
        return render(request, 'accounts/notifications.html', {'notifications': notify_objs, 'notification_count': get_notify_count(request.user)})
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
            return render(request, 'accounts/notifications.html', {'notifications': notifications, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
