from django.contrib.auth.models import AbstractUser
from django.db import models

def user_directory_path(instance, filename):
    return f'user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='user_images/',
        default='user_images/Default.jpg',
        blank=True
    )
