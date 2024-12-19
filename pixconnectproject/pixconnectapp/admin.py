from django.contrib import admin
from .models import CustomUser, PhotomanDetails, PhotographyImages, UserProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PhotomanDetails)
admin.site.register(PhotographyImages)
admin.site.register(UserProfile)

