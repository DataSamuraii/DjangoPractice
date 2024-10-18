from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_banned = models.BooleanField(default=False)
    bio = models.CharField(max_length=200, blank=True, null=True, default=None)

    def __str__(self):
        return self.username


class UnbanRequest(models.Model):
    UNBAN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=UNBAN_STATUS_CHOICES, default='pending')
