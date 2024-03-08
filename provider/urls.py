from django.urls import path
from . import views

urlpatterns = [
    path("home", views.homePage),
    path("new", views.newPost),
    path("requests",views.requestsViewAll),
    path("all_posts",views.allPosts)

]