from django.db import models

from fcm_django.models import FCMDevice


class FirebaseDeviceMixin:

    @property
    def devices(self):
        return FCMDevice.objects.filter(user=self)