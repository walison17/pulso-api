from fcm_django.api.rest_framework import FCMDeviceViewSet
from django.db.models import Count, Q
from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import status

from fcm_django.models import FCMDevice

from .serializers import FirebaseDeviceSerializer, NotificationSerializer


class FirebaseDeviceViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FirebaseDeviceSerializer

    def get_queryset(self):
        return FCMDevice.objects.filter(user=self.request.user, active=True)

    def perform_create(self, serializer):
        serializer = serializer.save(user=self.request.user)
        super(FirebaseDeviceViewSet, self).perform_create(serializer)


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        query = self.request.query_params.get('unread')
        notifications = user.notifications.all()
        if query:
            return notifications.filter(unread=query)

        return notifications

    @list_route(methods=['post'], url_path='mark_as_read')
    def mark_as_read(self, request):
        user = self.request.user
        user.notifications.filter(timestamp__lt=timezone.now()).mark_all_as_read()
        return Response(status=status.HTTP_204_NO_CONTENT)
