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


    def update(self, instance, validated_data):
        instance.about = validated_data.get('about', instance.about)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance

    
class FriendSerializer(serializers.Serializer):
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ('to_user', 'created')

