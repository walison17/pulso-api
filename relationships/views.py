from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import User
from .serializers import FolloweeSerializer, FollowSerializer


class FollowingView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()    
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FollowSerializer
        return FolloweeSerializer


    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowerView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FolloweeSerializer

    def get_queryset(self):
        return self.request.user.followers.all()


    