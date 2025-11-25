from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Blog
from subscriptions.models import UserSubscription # Import UserSubscription
from subscriptions.serializers import UserSubscriptionSerializer # Import UserSubscriptionSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    subscription_status = serializers.SerializerMethodField()
    subscription_plan = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_picture',
            'subscription_status',
            'subscription_plan',
        ]
        read_only_fields = ['id']

    def get_subscription_status(self, obj):
        try:
            return obj.usersubscription.status
        except UserSubscription.DoesNotExist:
            return None

    def get_subscription_plan(self, obj):
        try:
            if hasattr(obj, 'usersubscription') and obj.usersubscription.plan:
                return UserSubscriptionSerializer(obj.usersubscription).data['plan']
            return None
        except UserSubscription.DoesNotExist:
            return None


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2', None)
        password = validated_data.pop('password')
        # Default username to email if not provided
        username = validated_data.get('username')
        if not username:
            validated_data['username'] = validated_data['email']
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class EmailTokenObtainPairSerializer(serializers.Serializer):
    """JWT login using email + password for CustomUser that still uses username internally."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': _('No active account found with the given credentials')})

        if not user.is_active:
            raise serializers.ValidationError({'email': _('This account is inactive')})

        if not user.check_password(password):
            raise serializers.ValidationError({'password': _('No active account found with the given credentials')})

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data,
        }


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'author', 'title','cover_image', 'content', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'status', 'created_at', 'updated_at']


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'status', 'cover_image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        instance = getattr(self, 'instance', None)

        # Non-staff cannot set status directly
        if not (user and user.is_staff):
            if 'status' in attrs:
                raise serializers.ValidationError({'status': _('Only admins can change status.')})

        # If editing an existing post and it's already approved/denied, only staff can edit
        if instance is not None:
            if instance.status in (Blog.Status.APPROVED, Blog.Status.DENIED) and not (user and user.is_staff):
                raise serializers.ValidationError(_('You cannot modify a post that has been moderated.'))
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        blog = Blog.objects.create(author=user, status=Blog.Status.PENDING, **validated_data)
        return blog

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        # Authors can update title/content while pending; staff can update including status
        if user and user.is_staff:
            # staff can change any field
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
        else:
            # block status changes by non-staff
            validated_data.pop('status', None)
            for field in ['title', 'content']:
                if field in validated_data:
                    setattr(instance, field, validated_data[field])
        instance.save()
        return instance
