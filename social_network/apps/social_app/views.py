from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, LoginSerializer, UserSearchSerializer, FriendRequestSerializer, FriendPendingRequestSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import FriendRequest, Friendship
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404

# Get the user model defined in the Django project
User = get_user_model()

# View for user registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# View for user login
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # Generate or retrieve a token for the authenticated user
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.pk,
            "email": user.email
        })

# View for user logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the authentication token associated with the current user
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"message": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)

# Pagination class for user search
class UserSearchPagination(PageNumberPagination):
    page_size = 10

# View for searching users
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    pagination_class = UserSearchPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_keyword = self.request.query_params.get('search')
        user = self.request.user
        if search_keyword:
            # Filter users by email or username based on the search keyword
            queryset = User.objects.filter(email__iexact=search_keyword).exclude(id=user.id)
            if not queryset.exists():
                queryset = User.objects.filter(username__icontains=search_keyword).exclude(id=user.id)
            return queryset
        return User.objects.exclude(id=user.id)

# View for sending friend requests
class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        email_or_username = request.data.get('email_or_username')
        if not email_or_username:
            raise ValidationError({"error": "Email or Username is required"})
        
        try:
            to_user = User.objects.get(Q(email=email_or_username) | Q(username=email_or_username))
        except User.DoesNotExist:
            raise ValidationError({"error": "User does not exist"})
        
        from_user = request.user
        
        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            raise ValidationError({"error": "Friend request already sent"})
        
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=from_user, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({"error": "Too many requests. Please wait a while before sending more friend requests."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        
        return Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK) 

# View for accepting friend requests
class AcceptFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        email_or_username = request.data.get('email_or_username')
        if not email_or_username:
            raise ValidationError({"error": "Email or Username is required"})
        
        from_user = get_object_or_404(User, Q(email=email_or_username) | Q(username=email_or_username))
        to_user = request.user
        
        friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=to_user, accepted=False)
        
        friend_request.accepted = True
        friend_request.save()
        
        friendship = Friendship(user1=from_user, user2=to_user)
        friendship.save()
        
        response_data = {
            "message": "Friend request accepted",
            "friend_request": self.get_serializer(friend_request).data
        }
        return Response(response_data, status=status.HTTP_200_OK)

# View for rejecting friend requests
class RejectFriendRequestView(mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        email_or_username = request.data.get('email_or_username')
        if not email_or_username:
            return Response({"error": "Email or Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        from_user = get_object_or_404(User, Q(email=email_or_username) | Q(username=email_or_username))
        to_user = request.user
        
        friend_request = get_object_or_404(FriendRequest, from_user=from_user, to_user=to_user, accepted=False)
        
        if friend_request.to_user != request.user:
            raise PermissionDenied({"error": "You are not authorized to reject this request"})
        
        self.perform_destroy(friend_request)
        return Response({"message": "Friend request rejected successfully."}, status=status.HTTP_200_OK)

# View for listing user's friends
class ListFriendsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        friendships = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        friends_ids = [friendship.user1.id if friendship.user1 != user else friendship.user2.id for friendship in friendships]
        return User.objects.filter(id__in=friends_ids)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "You have no friends yet."}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# View for listing pending friend requests
class ListPendingRequestsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendPendingRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, accepted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "No pending friend requests"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
