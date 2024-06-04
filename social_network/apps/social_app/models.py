from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

# Custom user model extending AbstractUser
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Define many-to-many relationship for friendships
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False, related_name='friends_with')

    def __str__(self):
        return self.email


# Model for friend requests
class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def save(self, *args, **kwargs):
        # Ensure users cannot send friend requests to themselves
        if self.from_user == self.to_user:
            raise ValidationError("Users cannot send friend requests to themselves.")
        super(FriendRequest, self).save(*args, **kwargs)

    def __str__(self):
        return f"FriendRequest(from={self.from_user}, to={self.to_user}, accepted={self.accepted})"


# Model for friendships
class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friends1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friends2', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"Friendship({self.user1}, {self.user2})"

