from django.urls import path
from .views import (
    AdminLoginView,
    AdminMeView,
    AdminBlogListCreateView,
    AdminBlogDetailView,
)

urlpatterns = [
    # Auth
    path('auth/login/', AdminLoginView.as_view(), name='admin-auth-login'),
    path('auth/me/', AdminMeView.as_view(), name='admin-auth-me'),

    # Blog management
    path('blog/', AdminBlogListCreateView.as_view(), name='admin-blog-list-create'),
    path('blog/<int:pk>/', AdminBlogDetailView.as_view(), name='admin-blog-detail'),
]
