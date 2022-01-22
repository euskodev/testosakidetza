from django.db import models
from django.contrib.auth.models import User
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)

class TokenToUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=34, null=True, blank=False)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,
                                verbose_name='Registration date')

    def __str__(self):
        return self.user.username
        