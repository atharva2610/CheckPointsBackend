
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_checkpoints.urls')),
    path('apis/', include('app_api_checkpoints.urls')),
]