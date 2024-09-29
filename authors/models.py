from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, default='', blank=True)
