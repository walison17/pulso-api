from django.dispatch import receiver, Signal

from fcm_django.models import FCMDevice

user_was_followed = Signal(providing_args=['followee', 'follower'])

@receiver(user_was_followed)
def notify_new_follower(sender, follower, followee, **kwargs):
    devices = FCMDevice.objects.filter(user=followee)
    if devices.exists():
        devices.send_message(
            title=f'{follower.first_name} seguiu você'
        )
        