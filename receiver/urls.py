from django.urls import path
from . import views

app_name = "receiver"

urlpatterns = [
  
  path("home/", views.home,name="home"),
  path("view_post/<int:post_id>/", views.view_post,name="view_post"),
  path("order/", views.order, name="order"),
  path("wait/",views.waiting_page,name="waiting_page"),
  path("order-history/",views.order_history,name="order_history"),
  path("track-order/id=<int:ord_id>/",views.track_order,name="track_order"),
  path("feedback/id=<int:post_id>/",views.feedback,name="feedback"),
  path("send_feedback/",views.send_feedback,name="send_feedback"),
  path("logout",views.logout,name="logout"),
  path("order-delivered/id=<int:ord_id>/",views.order_delivered,name="order_delivered"),
  path("update-order/<int:post_id>/", views.update_order, name="update_order"),
  path("get_post_details/<int:post_id>/", views.get_post_details, name="get_post_details")
]