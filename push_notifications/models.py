from django.db import models
from django.conf import settings

from fcm_django.models import FCMDevice


class FirebaseDeviceMixin:

    @property
    def devices(self):
        return FCMDevice.objects.filter(user=self)


class DeviceQuerySet(models.QuerySet):

    def from_user(self, user):
        return self.filter(user=user)

    def from_users(self, users):
        return self.filter(user__in=users)

    def player_ids(self):
        return self.values_list('one_signal_player_id', flat=True)

    def as_list(self):
        return list(self)


class Device(models.Model):
    IOS = 0
    ANDROID = 1
    DEVICE_TYPES = (
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    device_type = models.SmallIntegerField(
        choices=DEVICE_TYPES,
        default=ANDROID,
        db_index=True
    )
    device_model = models.CharField(max_length=100, blank=True)
    device_id = models.CharField(max_length=150, db_index=True, unique=True)
    one_signal_player_id = models.CharField(
        max_length=150, db_index=True, unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DeviceQuerySet.as_manager()
