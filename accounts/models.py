from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    about = models.TextField(verbose_name='Descrição do usuário', blank=True, null=True)
    photo = models.URLField(verbose_name='Foto do perfil', max_length=150, blank=True, null=True)
    gender = models.CharField(verbose_name='Gênero', max_length=15, null=True)
    city = models.CharField(verbose_name='Cidade', max_length=50, null=True)
    state = models.CharField(verbose_name='Estado', max_length=3, null=True)
    country = models.CharField(verbose_name='País', max_length=20, null=True) 
    
