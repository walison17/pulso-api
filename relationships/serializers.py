from rest_framework import serializers

from django.shortcuts import get_object_or_404

from accounts.models import User
from .models import Follow


class FolloweeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo_url', 'city', 'state')
    

class FollowSerializer(serializers.Serializer):
    followee_id = serializers.IntegerField(write_only=True)
    followee = FolloweeSerializer(read_only=True, source='to_user')
    created_at = serializers.DateTimeField(read_only=True)


    def create(self, validated_data):
        follower = validated_data['follower']
        followee = get_object_or_404(User, pk=validated_data['followee_id'])
        return Follow.objects.create(from_user=follower, to_user=followee)