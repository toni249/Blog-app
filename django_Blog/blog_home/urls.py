
"""django_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views
from .views import (
                PostListView,
                PostDetailView,
                PostCreateView,
                PostUpdateView,
                PostDeleteView,
                UserPostListView
                )

from django.contrib.auth import views as auth_views 



urlpatterns = [
	# path('', views.home,name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
     path('post/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='new-post'),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name='post-delete'),
    path('profile/',views.profile,name='user-profile'),
    path('register/',views.register,name='user-register'),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name='user-login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'),name='user-logout'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html'
         ),
         name='password-reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ),
         name='password_reset_complete'),



    # path('/login',views.login,name='user-register'),
]
