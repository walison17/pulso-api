from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    about = models.TextField(blank=True, null=True)
    photo_url = models.URLField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=3, null=True)
    country = models.CharField(max_length=20, null=True) 
    
