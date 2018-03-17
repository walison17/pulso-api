from django.dispatch import Signal, receiver

from .models import Comment
from fcm_django.models import FCMDevice


new_comment = Signal(providing_args=['pulso'])


@receiver(new_comment)
def notify_pulso_creator_from_new_comments(sender, pulso, **kwargs):
    creator_devices = FCMDevice.objects.filter(user=pulso.created_by)
    if creator_devices.exists():
        body = f'{}'
        extra = {
            'body': body,
            'notification_type': 'comment',
            'object_id': ''
        }
        creator_devices.send_message(
            title='Pulso',
            body=body,
            icon='notification_icon',
            sound='default',
            color='#6f41bf',
            extra=extra
        )
