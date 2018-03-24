from django.dispatch import receiver, Signal

from notifications.signals import notify
from fcm_django.models import FCMDevice

user_was_followed = Signal(providing_args=['followee', 'follower'])


@receiver(user_was_followed)
def notify_new_follower(sender, follower, followee, **kwargs):
    devices = FCMDevice.objects.filter(user=followee)
    if devices.exists():
        body = f'{follower.name} seguiu você'
        extra = {
            'body': body, 'notification_type': 'follower', 'object_id': follower.id
        }
        devices.send_message(
            title='Pulso',
            body=body,
            icon='notification_icon',
            sound='default',
            color='#6f41bf',
            data=extra,
        )


@receiver(user_was_followed)
def save_notify_on_db(sender, follower, followee, **kwargs):
    notify.send(sender=follower, recipient=followee, verb='seguiu você')
