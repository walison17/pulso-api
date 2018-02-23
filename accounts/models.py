from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.conf import settings

from relationships.models import Follow
from notifications.models import FirebaseDeviceMixin


class User(AbstractUser, FirebaseDeviceMixin):
    facebook_id = models.BigIntegerField(null=True)
    about = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=3, null=True)
    country = models.CharField(max_length=20, null=True) 
    photo_url = models.URLField(max_length=150, blank=True, null=True)
    facebook_url = models.URLField(null=True)
    instagram_url = models.URLField(null=True)
    following = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, 
        through='relationships.Follow',
        related_name='followers',
    )
    facebook_friends_ids = ArrayField(models.BigIntegerField(), blank=True, null=True)


    def follow(self, user):
        """"Segue um novo usuário"""
        return Follow.objects.create(from_user=self, to_user=user)

 
    def follows(self, user):
        """Verifica se o usuário já segue um outro usuário"""
        return Follow.objects.filter(from_user=self, to_user=user).exists()

    
    def is_followed_by(self, user):
        """Verifica se o usuário é seguido por um outro usuário"""
        return Follow.objects.filter(from_user=user, to_user=self).exists()
