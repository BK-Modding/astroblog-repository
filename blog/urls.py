from django.urls import path, include
from . import views

urlpatterns = [
    path('newpost/', views.newpost, name='newpost'),
    path('<int:post_id>/', views.blogpost, name='blogpost'),
    path('<int:post_id>/comment/', views.comment, name='comment'),
    path('<int:post_id>/deletecomment/<int:comment_id>/', views.deletecomment, name='deletecomment'),
    path('latest/', views.latestposts, name='latest'),
    path('approvals/', views.approvals, name='approvals'),
    path('<int:post_id>/approve/', views.approve, name='approve'),
    path('<int:post_id>/deny/', views.deny, name='deny'),
    path('<int:post_id>/star/', views.star, name='star'),
    path('<int:post_id>/unstar/', views.unstar, name='unstar'),
    path('<int:post_id>/keep/', views.keep, name='keep'),
    path('<int:post_id>/unkeep/', views.unkeep, name='unkeep'),
    path('<int:post_id>/modify/', views.modifypost, name='modifypost'),
    path('keep/<int:keep_id>/makepublic/', views.makekeeppublic, name='makekeeppublic'),
    path('keep/<int:keep_id>/makeprivate/', views.makekeepprivate, name='makekeepprivate'),
    path('<int:post_id>/delete/', views.delete, name='delete'),
    path('user/<int:user_id>/userposts', views.userposts, name='userposts'),
    path('user/<int:user_id>/keeps/', views.userkeeps, name='userkeeps'),
    path('category/<str:category>/', views.categoryposts, name='categoryposts'),
    path('comments/', include('django_comments.urls'))
]
