from django.urls import path
from .views import (
    AdminLoginView,
    AdminMeView,
    AdminBlogListCreateView,
    AdminBlogDetailView,
    AdminUserListView,
    AdminUserDetailView,
    AdminBookListView,
    AdminBookDetailView,
    AdminSubscriptionPlanListView,
    AdminSubscriptionPlanDetailView
)

urlpatterns = [
    # Auth
    path('auth/login/', AdminLoginView.as_view(), name='admin-auth-login'),
    path('auth/me/', AdminMeView.as_view(), name='admin-auth-me'),

    # Blog management
    path('blog/', AdminBlogListCreateView.as_view(), name='admin-blog-list-create'),
    path('blog/<int:pk>/', AdminBlogDetailView.as_view(), name='admin-blog-detail'),

    # User management
    path('users/', AdminUserListView.as_view(), name='admin-user-list-create'),
    path('users/<int:pk>/', AdminUserDetailView.as_view(), name='admin-user-detail'),

    # Book management
    path('books/', AdminBookListView.as_view(), name='admin-book-list-create'),
    path('books/<int:pk>/', AdminBookDetailView.as_view(), name='admin-book-detail'),

    # Subscription Plan management
    path('subscription-plans/', AdminSubscriptionPlanListView.as_view(), name='admin-subscription-plan-list-create'),
    path('subscription-plans/<int:pk>/', AdminSubscriptionPlanDetailView.as_view(), name='admin-subscription-plan-detail'),
]
