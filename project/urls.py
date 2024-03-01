from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('admin_mod.urls')),
    path('superadmin/', admin.site.urls),
    paproviderth('/', include('provider.urls')),
    path('receiver/', include('receiver.urls')),
    # path('admin/', include('admin_mod.urls')),
]
