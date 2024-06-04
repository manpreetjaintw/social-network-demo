from django.urls import path
from .views import RegisterView, LoginView, LogoutView,UserSearchView,FriendRequestView,ListFriendsView,ListPendingRequestsView,AcceptFriendRequestView,RejectFriendRequestView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-requests/send/', FriendRequestView.as_view(), name='send_friend_request'),
    path('friend-requests/accept/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('friend-requests/reject/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/pending/', ListPendingRequestsView.as_view(), name='list_pending_requests'),

]
