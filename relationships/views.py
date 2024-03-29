from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView, ListAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from accounts.models import User

from .models import Follow
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


class FollowerListView(ListAPIView):
    serializer_class = FolloweeSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.followers.all()


class FollowingListView(ListAPIView):
    serializer_class = FolloweeSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.following.all()


class UnfollowView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_destroy(self, instance):
        rel = Follow.objects.get(from_user=self.request.user, to_user=instance)
        rel.delete()
