from rest_framework import serializers

from fcm_django.models import FCMDevice
from notifications.models import Notification
from accounts.models import User


class FirebaseDeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = FCMDevice
        fields = ('id', 'device_id', 'registration_id', 'type')
        read_only = ('id', 'device_id')

    def create(self, validated_data):
        try:
            device = FCMDevice.objects.get(device_id=validated_data.get('device_id'))
            device.registration_id = validated_data.get('registration_id')
            device.save()
        except FCMDevice.DoesNotExist:
            device = FCMDevice.objects.create(**validated_data)
        return device

    def update(self, instance, validated_data):
        instance.registration_id = validated_data.get('registration_id')
        instance.save()
        return instance


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo_url')


class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'timesince')
