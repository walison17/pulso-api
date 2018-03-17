from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from fcm_django.models import FCMDevice
from notifications.signals import notify
from comments.models import Comment


canceled_pulso = Signal(providing_args=['pulso'])
closed_pulso = Signal(providing_args=['pulso'])
new_pulso_interaction = Signal(providing_args=['pulso', 'author'])


@receiver(canceled_pulso)
def notify_users_from_cancellation(sender, pulso, **kwargs):
    pass


@receiver(post_save, sender=Comment)
def notify_creator_about_new_interaction(sender, instance, **kwargs):
    creator_devices = FCMDevice.objects.filter(user=instance.pulso.created_by)
    if creator_devices.exists():
        body = f'{instance.author.name} comentou seu pulso.'
        extra = {
            'body': body,
            'notification_type': 'INTERACTION',
            'object_id': instance.pulso.id
        }
        creator_devices.send_message(
            title='Pulso',
            body=body,
            icon='notification_icon',
            sound='default',
            color='#6f41bf',
            data=extra
        )


@receiver(post_save, sender=Comment)
def save_interaction_on_db(sender, instance, **kwargs):
    notify.send(
        sender=instance.author,
        recipient=instance.pulso.created_by,
        verb='comentou seu pulso'
    )
