from django.urls import path
from . import views


app_name = "provider"
urlpatterns = [
    path("home", views.homePage, name="homepage"),
    path("new", views.newPost),
    path("requests",views.requestsViewAll, name="requests"),
    path("all_posts",views.allPosts, name="allposts"),
    path("feedback/<int:post_id>", views.feedback, name="feedback"),
    path("accept/<int:order_id>", views.accept, name="accept"),
    path("reject/<int:order_id>", views.reject, name="reject"),
    path("delete/<int:post_id>", views.delete_post, name="deletion")

]