from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 
            'email',
            'first_name', 
            'last_name', 
            'photo_url', 
            'facebook_url',
            'gender', 
            'city', 
            'state',
            'country', 
            'about',
            'following_count'
        )
        read_only_fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'gender',
            'facebook_url',
            'photo_url',
            'following_count'
        )


    def get_following_count(self, obj):
        return obj.following.count()


    def update(self, instance, validated_data):
        instance.about = validated_data.get('about', instance.about)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance

    