from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("login", views.login),
    path("register", views.register),
    path("adminPanel", views.adminPanel),
    path("wait", views.waitingPage),
    path('approve_user/<int:user_id>/', views.approve_user, name='approve_user'),
    path('reject_user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('check_user_existence/', views.check_user_existence, name='check_user_existence')

]