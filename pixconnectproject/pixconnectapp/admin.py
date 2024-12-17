from django.contrib import admin
from .models import CustomUser, PhotomanDetails, PhotographyImages

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(PhotomanDetails)
admin.site.register(PhotographyImages)

