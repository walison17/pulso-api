from django.shortcuts import get_object_or_404
from rest_framework import serializers

from friendship.models import Friend, FriendshipRequest

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'email',
            'first_name', 
            'last_name', 
            'photo_url', 
            'gender', 
            'city', 
            'state',
            'country', 
            'about',
        )
        read_only_fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
        )

    
class FriendSerializer(serializers.Serializer):
    id = serializers.IntegerField() 



class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('viewed',)
