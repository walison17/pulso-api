from django.dispatch import receiver

from relationships.models import Follow, new_follower


@receiver(new_follower)
def send_notification(sender, follower, followee, **kwargs):
    followee.devices.exists():
        followee.devices.send_notification(
            title=f'{follower.first_name} seguiu você'
        )