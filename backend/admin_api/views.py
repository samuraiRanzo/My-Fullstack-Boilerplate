from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import Blog
from core.serializers import BlogSerializer
from .serializers import (
    AdminEmailTokenObtainPairSerializer,
    AdminBlogWriteSerializer,
)


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
