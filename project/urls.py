from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('provide/', include('provider.urls')),
    path('receive/', include('receiver.urls')),
    path('admin/', include('admin_mod.urls')),
]
