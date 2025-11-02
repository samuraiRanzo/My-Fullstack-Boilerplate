from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Blog
from core.serializers import BlogSerializer

User = get_user_model()


class AdminEmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': _('No active account found with the given credentials')})

        if not user.is_active or not user.check_password(password):
            raise serializers.ValidationError({'password': _('No active account found with the given credentials')})

        if not (user.is_staff or user.is_superuser):
            raise PermissionDenied('Admin access only.')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        }


class AdminBlogWriteSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='author', required=False
    )

    class Meta:
        model = Blog
        fields = ['id', 'author_id', 'title', 'content', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
