from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import FriendRequest, Friendship


User = get_user_model()

# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # Check if passwords match
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Create user object with validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Serializer for user login
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


# Serializer for user search
class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Serializer for friend requests
class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = '__all__'


# Serializer for pending friend requests
class FriendPendingRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'timestamp', 'accepted']

    def get_from_user(self, obj):
        return {
            'id': obj.from_user.id,
            'username': obj.from_user.username,
            'email': obj.from_user.email
        }
