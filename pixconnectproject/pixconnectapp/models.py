from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# For All
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('photographer', 'Photographer'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
