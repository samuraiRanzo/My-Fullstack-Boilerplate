from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # path('hello/', views.hello, name='hello'),

    # Auth endpoints
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'),
    path('auth/login/', views.EmailLoginView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/user/', views.UserView.as_view(), name='auth-user'),
    path('auth/user/profile-picture/', views.ProfilePictureUploadView.as_view(), name='profile-picture-upload'),

    # Blog endpoints
    path('blog/', views.BlogListCreateView.as_view(), name='blog-list-create'),
    path('blog/my/', views.MyBlogListView.as_view(), name='blog-my-list'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
]
