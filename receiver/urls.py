from django.urls import path
from . import views

urlpatterns = [
  path("", views.dashboard,name="receiver"),
  path("view_post/<int:post_id>/", views.view_post,name="view_post"),
  path("order/id=<int:post_id>/", views.order, name="order"),
]