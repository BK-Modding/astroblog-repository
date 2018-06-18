"""astroblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
import blog.views
import accounts.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', blog.views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('posts/', include('blog.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('captcha/', include('captcha.urls')),
    path('query/', views.query, name='query'),
    path('query/viewqueries/', views.viewqueries, name='viewqueries'),
    path('query/<int:query_id>/reply', views.replyquery, name='replyquery'),
    path('query/<int:query_id>/delete', views.deletequery, name='deletequery'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('user/<int:user_id>/', views.userdetails, name='userdetails'),
    path('user/<int:user_id>/changedp', views.changedp, name='changedp'),
    path('user/<int:user_id>/changedesc', views.changedesc, name='changedesc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
