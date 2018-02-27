from django.dispatch import receiver, Signal
from django.urls import reverse_lazy

from fcm_django.models import FCMDevice

user_was_followed = Signal(providing_args=['followee', 'follower'])

@receiver(user_was_followed)
def notify_new_follower(sender, follower, followee, **kwargs):
    devices = FCMDevice.objects.filter(user=followee)
    if devices.exists():
        data_message = {
            'title': f'{follower.name} seguiu você',
            'notification_type': 'follower',
            'follower_id': follower.id
        }
        devices.send_message(data=data_message)
        