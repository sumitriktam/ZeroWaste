from django.urls import path
from . import views

urlpatterns = [
    path("home", views.homePage),
    path("new", views.newPost),
    path("requests",views.requestsViewAll)

]