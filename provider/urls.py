from django.urls import path
from . import views


app_name = "provider"
urlpatterns = [
    path("home", views.homePage),
    path("new", views.newPost),
    path("requests",views.requestsViewAll),
    path("all_posts",views.allPosts),
    path("feedback/<int:post_id>", views.feedback, name="feedback")

]