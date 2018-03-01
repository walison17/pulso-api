from django.dispatch import receiver, Signal

from notifications.signals import notify
from fcm_django.models import FCMDevice

user_was_followed = Signal(providing_args=['followee', 'follower'])


@receiver(user_was_followed)
def notify_new_follower(sender, follower, followee, **kwargs):
    notify.send(sender=follower, recipient=followee, verb='seguiu você')
    devices = FCMDevice.objects.filter(user=followee)
    if devices.exists():
        title = f'{follower.name} seguiu você'
        extra = {
            'title': title,
            'notification_type': 'follower',
            'object_id': follower.id,
        }
        devices.send_message(title=title, data=extra)
