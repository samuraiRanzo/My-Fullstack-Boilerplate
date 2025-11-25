from django.urls import path, include

urlpatterns = [
    path('api/', include('core.urls')),
    path('api/admin-api/', include('admin_api.urls')),
    path('api/todos/', include('todos.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/books/', include('books.urls')),
]
