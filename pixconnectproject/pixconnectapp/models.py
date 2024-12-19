from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# For All
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('photographer', 'Photographer'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


# Photographer Section
class PhotomanDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    aadhar_image = models.ImageField(upload_to='aadhar_images/')
    place = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PhotographyImages(models.Model):
    photographer = models.ForeignKey(PhotomanDetails, on_delete=models.CASCADE, related_name='working_images')
    image = models.ImageField(upload_to='working_images/')
    spot = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)   
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.photographer.first_name} {self.photographer.last_name} at {self.spot}"


# User Section
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=False, default='0000000000')
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
