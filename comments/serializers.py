from rest_framework import serializers

from .models import Comment
from accounts.models import User


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo_url')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_at')
        read_only = ('created_at', )

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
