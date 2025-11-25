from http import HTTPStatus

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Blog
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    EmailTokenObtainPairSerializer,
    BlogSerializer,
    BlogCreateUpdateSerializer,
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=201)


class EmailLoginView(TokenObtainPairView):
    """JWT login using email + password"""
    permission_classes = [AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # Prefetch the related UserSubscription object
        user = User.objects.select_related('usersubscription').get(pk=user.pk)
        return Response(UserSerializer(user).data)


class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Public sees only approved posts
        return Blog.objects.filter(status=Blog.Status.APPROVED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogCreateUpdateSerializer
        return BlogSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class BlogDetailView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.select_related('author').all()
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return BlogCreateUpdateSerializer
        return BlogSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_object(self):
        obj = super().get_object()
        # If not approved, only author or staff can view
        if obj.status != Blog.Status.APPROVED:
            user = self.request.user
            if not (user.is_authenticated and (user.is_staff or user == obj.author)):
                from rest_framework.exceptions import NotFound
                raise NotFound()
        return obj

    def perform_update(self, serializer):
        obj = self.get_object()
        user = self.request.user
        # Author or staff may update; non-author cannot.
        if not (user.is_staff or user == obj.author):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('You do not have permission to edit this post.')
        serializer.save()


class MyBlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)


class ProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


