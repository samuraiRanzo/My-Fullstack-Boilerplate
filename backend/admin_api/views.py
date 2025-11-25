from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Blog
from core.serializers import BlogSerializer
from books.models import Book # Import Book model
from subscriptions.models import SubscriptionPlan # Import SubscriptionPlan model
from .serializers import (
    AdminEmailTokenObtainPairSerializer,
    AdminBlogWriteSerializer,
    AdminUserSerializer,
    AdminBookSerializer,
    AdminSubscriptionPlanSerializer, # Import the new serializer
)
from django.contrib.auth import get_user_model # Import get_user_model

User = get_user_model() # Get the custom user model


class AdminLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = AdminEmailTokenObtainPairSerializer


class AdminMeView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        u = request.user
        return Response({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'is_staff': u.is_staff,
            'is_superuser': u.is_superuser,
        })


class AdminPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AdminBlogListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pagination_class = AdminPagination

    def get_queryset(self):
        qs = Blog.objects.select_related('author').all().order_by('-created_at')
        status_param = self.request.query_params.get('status')
        author_id = self.request.query_params.get('author_id')
        if status_param:
            qs = qs.filter(status=status_param)
        if author_id:
            qs = qs.filter(author_id=author_id)
        return qs

    def get_serializer_class(self):
        return AdminBlogWriteSerializer if self.request.method == 'POST' else BlogSerializer

    def perform_create(self, serializer):
        # If no author is provided, default to the admin creating it
        if 'author' not in serializer.validated_data or serializer.validated_data.get('author') is None:
            serializer.save(author=self.request.user)
        else:
            serializer.save()


class AdminBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Blog.objects.select_related('author').all()

    def get_serializer_class(self):
        return AdminBlogWriteSerializer if self.request.method in ('PUT', 'PATCH') else BlogSerializer

# New User Management Views
class AdminUserListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    pagination_class = AdminPagination

class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer

# New Book Management Views
class AdminBookListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = AdminBookSerializer
    pagination_class = AdminPagination

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

class AdminBookDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = AdminBookSerializer

# New Subscription Plan Management Views
class AdminSubscriptionPlanListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = SubscriptionPlan.objects.all().order_by('price')
    serializer_class = AdminSubscriptionPlanSerializer
    pagination_class = AdminPagination

class AdminSubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = SubscriptionPlan.objects.all()
    serializer_class = AdminSubscriptionPlanSerializer
