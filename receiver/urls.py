from django.urls import path
from . import views

urlpatterns = [
  path("", views.dashboard,name="receiver"),
  path("view_post/<int:post_id>/", views.view_post,name="view_post"),
  path("order/", views.order, name="order"),
  path("track-order/id=<int:post_id>/",views.track_order,name="track_order"),
  path("order-history/",views.order_history,name="order_history")
]