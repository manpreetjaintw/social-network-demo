from django.contrib import admin
from .models import CustomUser,Friendship,FriendRequest

admin.site.register(CustomUser)
admin.site.register(Friendship)
admin.site.register(FriendRequest)

