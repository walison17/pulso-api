from fcm_django.api.rest_framework import FCMDeviceViewSet

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceSerializer

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
        return self.request.user.notifications.all()
