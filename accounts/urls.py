from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('<int:user_id>/changepassword/', views.changepassword, name='changepassword'),
    path('<int:user_id>/notifications/', views.notifications, name='notifications'),
    path('<int:user_id>/notifications/dismiss/<int:notify_id>/', views.dismiss_notification, name='dismiss_notification')
]