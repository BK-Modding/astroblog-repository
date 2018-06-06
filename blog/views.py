from random import shuffle
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm
from accounts.models import Notification

# Create your views here.
def index(request):
    results = list(Post.objects.filter(is_approved=True))
    shuffle(results)
    return render(request, 'blog/index.html', {'posts': results})

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
            return render(request, 'blog/newpost.html', {'post_error': 'Error, Some fields have not been filled', 'form': form})



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

def blogpost(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author.username == request.user.username or request.user.is_staff:
        starred = False
        if request.user.is_staff:
            starred_users = Post.objects.values_list('starredby', flat=True).all()
            print(starred_users)
            print(request.user.pk)
            if request.user.pk in starred_users:
                starred = True
        return render(request, 'blog/post.html', {'post': post, 'starred': starred})
    else:
        if not post.is_approved:
            return redirect('index')
        else:
            starred = False
            starred_users = Post.objects.values_list('starredby', flat=True).all()
            if request.user.pk in starred_users:
                starred = True
            return render(request, 'blog/post.html', {'post': post, 'starred': starred})

@login_required   
def comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if request.POST['commentarea']:
            new_comment = Comment()
            new_comment.comment = request.POST['commentarea']
            new_comment.commenter = request.user
            new_comment.save()
            post.save()
            post.comments.add(new_comment)
            post.save()
            return render(request, 'blog/post.html', {'post': post})
        else:
            return render(request, 'blog/post.html', {'post': post})
            
            
def latestposts(request):
    latest = Post.objects.filter(is_approved=True).order_by('-dateandtime')
    return render(request, 'blog/latestposts.html', {'posts': latest})
    
@login_required()
def approvals(request):
    if request.user.is_staff:
        posts_to_approve = Post.objects.filter(is_approved=False).order_by('-dateandtime')
        return render(request, 'blog/approvals.html', {'posts': posts_to_approve})
    else:
        return redirect('index')
        
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
            return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'approved_post': post_to_approve})
        else:
            return redirect('index')
        
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
                return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'denied_post': post_to_deny})
            else:
                return render(request, 'blog/approvals.html', {'posts': posts_to_approve, 'denied_error': post_to_deny})

@login_required
def star(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.totalstars += 1
        notify_author = Notification()
        notify_author.user_to_notify = post.author
        notify_author.content = request.user.username + ''' starred your post titled <a href="\posts\\''' + str(post_id) + '''">''' + post.title + '''</a>''' ################ USSSSSSSSSSSSERRRRRRRRRRRRRRRR PAGGGGGGGGGGGGGE FOR STARRING NOTIFY
        notify_author.save()
        post.save()
        post.starredby.add(request.user)
        post.save()
        return redirect('blogpost', post_id)
    
@login_required
def unstar(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        post.totalstars -= 1
        post.save()
        post.starredby.remove(request.user)
        post.save()
        return redirect('blogpost', post_id)