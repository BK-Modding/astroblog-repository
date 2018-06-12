from random import shuffle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Post, Comment, Keep
from .forms import PostForm
from accounts.models import Notification, UserProfile

'''category_dict = {
        'Stars and Planets': 'STARS&PLANETS',
        'Neutron stars and Pulsars': 'PULSARS',
        'Black holes and Quasars': 'QUASARS',
        'Galaxies and Cosmology': 'GALAXIES&COSMOLOGY',
        'Relativity in Astro' : 'RELATIVITY',
        'Particle Physics and Quantum Mechanics in Astro': 'PARTICLE&QM',
        'String Theory in Astro': 'STRINGTHEORY',
        'Astronomy': 'ASTRONOMY',
        'Scientific Literature': 'SCIENTIFIC_LITERATURE'
    }'''
    
def get_notify_count(user):
    usernotifications = None
    if user.is_authenticated:
        usernotifications = Notification.objects.filter(user_to_notify=user, dismissed=False).count()
    
    return usernotifications

# Create your views here.
def index(request):
    results = list(Post.objects.filter(is_approved=True))
    shuffle(results)
    return render(request, 'blog/index.html', {'posts': results, 'notification_count': get_notify_count(request.user)})

@login_required()
def newpost(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blog/newpost.html', {'form': form})
    elif request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post()
            post.title = form.cleaned_data['title']
            post.dateandtime = timezone.datetime.now()
            post.intro = form.cleaned_data['intro']
            post.category = form.cleaned_data['category']
            post.author = request.user
            post.body = form.cleaned_data['body']
            post.image = form.cleaned_data['image']
            if request.user.is_staff:
                post.is_approved = True
            post.save()
            return redirect('blogpost', post_id=post.id)
        else:
            return render(request, 'blog/newpost.html', {'post_error': 'Error, Some fields have not been filled', 'form': form, 'notification_count': get_notify_count(request.user)})



'''if request.POST['title'] and request.POST['intro'] and request.FILES['image'] and request.POST['body']:
            post = Post()
            post.title = request.POST['title']
            post.dateandtime = timezone.datetime.now()
            post.intro = request.POST['intro']
            post.author = request.user
            post.body = request.POST['body']
            post.image = request.FILES['image']
        else:
            return render(request, 'blog/newpost.html', {'post_error': 'Error, Some fields have not been filled', 'form': form})
'''

@login_required
def delete(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user.id == post.author.id:
             notify_author = Notification()
             notify_author.user_to_notify = post.author
             notify_author.content = '''Your post titled <a href="\posts\\''' + str(post.id) + '''">''' + post.title + '''</a> has been deleted by you.'''
             notify_author.save()
             post.delete()
             return redirect('index')
        else:
            return redirect('unauthorized')
            
def blogpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated:
        keeps_count = Keep.objects.filter(blog_post=post).count()
        return render(request, 'blog/post.html', {'post': post, 'keeps_count': keeps_count})
    else:
        if post.author.username == request.user.username or request.user.is_staff:
            starred = False
            kept = False
            if request.user.is_staff:
                starred_user = Post.objects.filter(id=post.id, starredby=request.user)
                kept_user = Keep.objects.filter(blog_post=post, keep_user=request.user)
                if starred_user:
                    starred = True
                if kept_user:
                    kept = True
            keeps_count = Keep.objects.filter(blog_post=post).count()
            return render(request, 'blog/post.html', {'post': post, 'starred': starred, 'kept': kept, 'keeps_count': keeps_count, 'notification_count': get_notify_count(request.user)})
        else:
            if not post.is_approved:
                return redirect('index')
            else:
                starred = False
                kept = False
                starred_user = Post.objects.filter(id=post.id, starredby=request.user)
                kept_user = Keep.objects.filter(blog_post=post, keep_user=request.user)
                if starred_user:
                    starred = True
                if kept_user:
                    kept = True
                keeps_count = Keep.objects.filter(blog_post=post).count()
                return render(request, 'blog/post.html', {'post': post, 'starred': starred, 'kept': kept, 'keeps_count': keeps_count, 'notification_count': get_notify_count(request.user)})

@login_required   
def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if request.POST['commentarea']:
            new_comment = Comment()
            new_comment.comment = request.POST['commentarea']
            new_comment.commenter = request.user
            new_comment.comment_date_and_time = timezone.datetime.now()
            new_comment.save()
            post.save()
            post.comments.add(new_comment)
            post.save()
            return render(request, 'blog/post.html', {'post': post, 'notification_count': get_notify_count(request.user)})
        else:
            return render(request, 'blog/post.html', {'post': post, 'notification_count': get_notify_count(request.user)})

@login_required
def deletecomment(request, post_id, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.commenter:
            post = get_object_or_404(Post, pk=post_id)
            post.comments.remove(comment)
            post.save()
            comment.delete()
            return redirect('blogpost', post_id=post_id)
        else:
            return redirect('unauthorized')
            
            
def latestposts(request):
    latest = Post.objects.filter(is_approved=True).order_by('-dateandtime')
    return render(request, 'blog/latestposts.html', {'posts': latest, 'notification_count': get_notify_count(request.user)})
    
@login_required()
def approvals(request):
    if request.user.is_staff:
        posts_to_approve = Post.objects.filter(is_approved=False).order_by('-dateandtime')
        return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'notification_count': get_notify_count(request.user)})
    else:
        return redirect('unauthorized')
        
@login_required
def approve(request, post_id):
    if request.method == 'POST':
        if request.user.is_staff:
            post_to_approve = get_object_or_404(Post, pk=post_id)
            post_to_approve.is_approved = True
            post_to_approve.save()
            notify_author = Notification()
            notify_author.user_to_notify = post_to_approve.author
            notify_author.content = '''Your post titled <a href="\posts\\''' + str(post_to_approve.id) + '''">''' + post_to_approve.title + '''</a> has been approved by astroblog moderation.'''
            notify_author.save()
            posts_to_approve = Post.objects.filter(is_approved=False).order_by('-dateandtime')
            return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'approved_post': post_to_approve, 'notification_count': get_notify_count(request.user)})
        else:
            return redirect('unauthorized')
        
@login_required
def deny(request, post_id):
    if request.method == 'POST':
        if request.user.is_staff:
            if request.POST['moderation_comments']:
                post_to_deny = get_object_or_404(Post, pk=post_id)
                post_to_deny.is_denied = True
                post_to_deny.moderation_comments = request.POST['moderation_comments']
                post_to_deny.save()
                notify_author = Notification()
                notify_author.user_to_notify = post_to_deny.author
                notify_author.content = '''Your post titled <a href="\posts\\''' + str(post_to_deny.id) + '''">''' + post_to_deny.title + '''</a> has been denied by astroblog moderation. Visit the post to view moderation comments.'''
                notify_author.save()
                posts_to_approve = Post.objects.filter(is_approved=False).order_by('-dateandtime')
                return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'denied_post': post_to_deny, 'notification_count': get_notify_count(request.user)})
            else:
                return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'denied_error': post_to_deny, 'notification_count': get_notify_count(request.user)})

@login_required
def star(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user.username != post.author.username:
            post.totalstars += 1
            notify_author = Notification()
            notify_author.user_to_notify = post.author
            notify_author.content = '''<a href="{% url 'userdetails' ''' + str(request.user.id) + ''' %}">''' + request.user.username + '''</a> starred the post "<a href="\posts\\''' + str(post_id) + '''">''' + post.title + '''</a>"''' ################ (This is done lol) USSSSSSSSSSSSERRRRRRRRRRRRRRRR PAGGGGGGGGGGGGGE FOR STARRING NOTIFY
            notify_author.save()
            post.starredby.add(request.user)
            post.save()
        return redirect('blogpost', post_id)
    
@login_required
def unstar(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user.username != post.author.username:
            post.totalstars -= 1
            post.starredby.remove(request.user)
            post.save()
        return redirect('blogpost', post_id)
        
@login_required
def keep(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user.username != post.author.username:
            notify_author = Notification()
            notify_author.user_to_notify = post.author
            notify_author.content = '''<a href="{% url 'userdetails' ''' + str(request.user.id) + ''' %}">''' + request.user.username + '''</a> kept the post "<a href="\posts\\''' + str(post_id) + '''">''' + post.title + '''</a>"''' ################ (This is done lol) USSSSSSSSSSSSERRRRRRRRRRRRRRRR PAGGGGGGGGGGGGGE FOR STARRING NOTIFY
            notify_author.save()
            keep = Keep()
            keep.blog_post = post
            keep.keep_user = request.user
            keep.save()
        return redirect('blogpost', post_id)

@login_required
def unkeep(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        if request.user.username != post.author.username:
            keep = get_object_or_404(Keep, keep_user=request.user, blog_post=post)
            keep.delete()
        return redirect('blogpost', post_id)
        
@login_required
def makekeeppublic(request, keep_id):
    if request.method == 'POST':
        keep = get_object_or_404(Keep, pk=keep_id)
        if keep.keep_user == request.user:
            keep.is_private = False
            keep.save()
            return redirect('userdetails', user_id=request.user.id)
        else:
            return redirect('unauthorized')
        
@login_required
def makekeepprivate(request, keep_id):
    if request.method == 'POST':
        keep = get_object_or_404(Keep, pk=keep_id)
        if keep.keep_user == request.user:
            keep.is_private = True
            keep.save()
            return redirect('userdetails', user_id=request.user.id)
        else:
            return redirect('unauthorized')
        
def userposts(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    posts = Post.objects.filter(author=user)
    return render(request, 'blog/userposts.html', {'posts': posts, 'user': user, 'notification_count': get_notify_count(request.user)})

@login_required
def userkeeps(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(User, pk=user_id)
        keeps = Keep.objects.filter(keep_user=request.user)
        return render(request, 'blog/userkeeps.html', {'keeps': keeps, 'notification_count': get_notify_count(request.user)})
    else:
        return redirect('unauthorized')
    
def categoryposts(request, category):
    posts = Post.objects.filter(category=category).order_by('-dateandtime')
    return render(request, 'blog/categoryposts.html', {'posts': posts, 'category': category, 'notification_count': get_notify_count(request.user)})
    