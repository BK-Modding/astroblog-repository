from django.urls import path, include
from . import views

urlpatterns = [
    path('newpost/', views.newpost, name='newpost'),
    path('<int:post_id>/', views.blogpost, name='blogpost'),
    path('<int:post_id>/comment/', views.comment, name='comment'),
    path('latest/', views.latestposts, name='latest'),
    path('approvals/', views.approvals, name='approvals'),
    path('<int:post_id>/approve/', views.approve, name='approve'),
    path('<int:post_id>/deny/', views.deny, name='deny'),
    path('<int:post_id>/star/', views.star, name='star'),
    path('<int:post_id>/unstar/', views.unstar, name='unstar')
]
