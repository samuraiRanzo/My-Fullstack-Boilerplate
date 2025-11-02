from django.urls import path, include

urlpatterns = [
    path('api/', include('core.urls')),
    path('admin-api/', include('admin_api.urls')),
]
