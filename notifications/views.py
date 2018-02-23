from fcm_django.api.rest_framework import FCMDeviceViewSet

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from fcm_django.models import FCMDevice
from fcm_django.api.rest_framework import FCMDeviceSerializer

from .serializers import FirebaseDeviceSerializer


class FirebaseDeviceViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FirebaseDeviceSerializer


    def get_queryset(self):
        return FCMDevice.objects.filter(user=self.request.user, active=True)

    
    def perform_create(self, serializer):
        serializer = serializer.save(user=self.request.user)
        super(FirebaseDeviceViewSet, self).perform_create(serializer)
