from django.contrib import admin
# from admin_mod.views import custom_admin_site
from django.urls import path, include

urlpatterns = [
    path('', include('admin_mod.urls')),
    # path('superadmin/', custom_admin_site.urls),
    path('superadmin/', admin.site.urls),
    path('provider/', include('provider.urls', namespace="provider")),
    path('receiver/', include('receiver.urls', namespace="receiver")),
    # path('admin/', include('admin_mod.urls')),
]
