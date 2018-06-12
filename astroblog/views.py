from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import Query
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Notification, UserProfile
from blog.models import Post, Keep
from django.conf import settings
from django.core.mail import send_mail
try:
    from . import local_settings
except ImportError:
    print("import error")
    pass


def get_notify_count(user):
    usernotifications = None
    if user.is_authenticated:
        usernotifications = Notification.objects.filter(user_to_notify=user, dismissed=False).count()
    
    return usernotifications

def aboutus(request):
    return render(request, 'aboutus.html', {'notification_count': get_notify_count(request.user)})
    
def query(request):
    if request.method == 'GET':
        return render(request, 'query.html', {'notification_count': get_notify_count(request.user)})
    elif request.method == 'POST':
        if request.POST['name'] and request.POST['email'] and request.POST['querybody']:
            new_query = Query()
            new_query.name = request.POST['name']
            new_query.email = request.POST['email']
            new_query.body = request.POST['querybody']
            new_query.date_and_time_of_submission = timezone.datetime.now()
            new_query.save()
            return render(request, 'query.html', {'query_success': True, 'notification_count': get_notify_count(request.user)})
        else:
            return render(request, 'query.html', {'query_error': 'Error, some fields have not been filled', 'notification_count': get_notify_count(request.user)})

@login_required
def viewqueries(request):
    if request.method == 'GET':
        if request.user.is_staff:
            queries = Query.objects.filter(is_deleted=False)
            return render(request, 'queries.html', {'queries': queries, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
    
@login_required
def replyquery(request, query_id):
    if request.method == 'POST':
        if request.user.is_staff:
            query = get_object_or_404(Query, pk=query_id)
            query.is_answered = True
            query.moderation_reply = request.POST['query_response']
            query.save()
            queries = Query.objects.filter(is_deleted=False)
            subject = 'Your query has a response from Astroblog moderation'
            from_email = local_settings.DEFAULT_FROM_EMAIL
            message = ''
            recipient_list = [query.email, 'kavesbteja@gmail.com']
            html_message = '''<h3>Response to your query submitted on {}</h3>
            <h6>Your query: {} </h6>
            <hr>
            <h6>Moderation Response: {} </h6>
            <br>
            <br>
            <br>
            <em>Keep looking up to the stars!</em>'''.format(query.date_and_time_pretty, query.body, request.POST['query_response'])
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
            return render(request, 'queries.html', {'queries': queries, 'query_response': query, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
@login_required
def deletequery(request, query_id):
    if request.method == 'POST':
        if request.user.is_staff:
            query = get_object_or_404(Query, pk=query_id)
            query.is_deleted = True
            query.moderation_reply = request.POST['query_response']
            query.save()
            
            subject = 'Some subject'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = 'This is my test message'
            recipient_list = ['mytest@gmail.com', 'you@email.com']
            html_message = '<h1>This is my HTML test</h1>'
            
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)
            queries = Query.objects.filter(is_deleted=False)
            return render(request, 'queries.html', {'queries': queries, 'query_deletion': query, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
        
def unauthorized(request):
    return render(request, 'unauthorized.html', {'notification_count': get_notify_count(request.user)})
    
def userdetails(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    user_posts = Post.objects.filter(author=user)
    user_keeps = Keep.objects.filter(keep_user=user)
    return render(request, 'user.html', {'user_details': user, 'user_profile': user_profile, 'user_keeps': user_keeps, 'user_posts': user_posts, 'notification_count': get_notify_count(request.user)})

@login_required
def changedp(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        if request.user.id == user.id:
            if request.FILES['image']:
                user_profile = get_object_or_404(UserProfile, user=user)
                user_profile.profile_photo = request.FILES['image']
                user_profile.save()
            return redirect('userdetails', user_id=user_id)
        else:
            return redirect('unauthorized')

@login_required
def changedesc(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        if request.user.id == user.id:
            if request.POST['description']:
                user_profile = get_object_or_404(UserProfile, user=user)
                user_profile.profile_description = request.POST['description']
                user_profile.save()
            return redirect('userdetails', user_id=user_id)
        else:
            return redirect('unauthorized')
