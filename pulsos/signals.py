from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from fcm_django.models import FCMDevice
from notifications.signals import notify
from comments.models import Comment


canceled_pulso = Signal(providing_args=['pulso'])
closed_pulso = Signal(providing_args=['pulso'])
new_pulso_interaction = Signal(providing_args=['pulso', 'author'])


def send_notification(devices, body, data):
    devices.send_message(
        title='Pulso',
        body=body,
        icon='notification_icon',
        sound='default',
        color='#6f41bf',
        data=data,
    )


@receiver(closed_pulso)
def notify_users_about_closement(sender, pulso, **kwargs):
    participants_devices = FCMDevice.objects.filter(user__in=pulso.participants)
    if participants_devices.exists():
        body = f'{pulso.created_by.name} correspondeu o pulso.'
        extra = {'body': body, 'notification_type': 'CLOSEMENT', 'object_id': pulso.id}
        send_notification(participants_devices, body, extra)


@receiver(closed_pulso)
def save_closement_on_db(sender, pulso, **kwargs):
    for p in pulso.participants:
        notify.send(sender=pulso.created_by, recipient=p, verb='correspondeu o pulso.')


@receiver(canceled_pulso)
def notify_users_about_cancellation(sender, pulso, **kwargs):
    participants_devices = FCMDevice.objects.filter(user__in=pulso.participants)
    if participants_devices.exists():
        body = f'{pulso.created_by.name} cancelou o pulso.'
        extra = {
            'body': body, 'notification_type': 'CANCELLATION', 'object_id': pulso.id
        }
        send_notification(participants_devices, body, extra)


@receiver(canceled_pulso)
def save_cancellation_on_db(sender, pulso, **kwargs):
    for p in pulso.participants:
        notify.send(sender=pulso.created_by, recipient=p, verb='cancelou o pulso.')


@receiver(post_save, sender=Comment)
def notify_creator_about_new_interaction(sender, instance, **kwargs):
    pulso_creator = instance.pulso.created_by
    creator_devices = FCMDevice.objects.filter(user=pulso_creator)
    if pulso_creator != instance.author and creator_devices.exists():
        body = f'{instance.author.name} comentou seu pulso.'
        extra = {
            'body': body,
            'notification_type': 'INTERACTION',
            'object_id': instance.pulso.id,
        }
        send_notification(creator_devices, body, extra)


@receiver(post_save, sender=Comment)
def save_interaction_on_db(sender, instance, **kwargs):
    pulso_creator = instance.pulso.created_by
    if pulso_creator != instance.author:
        notify.send(
            sender=instance.author,
            recipient=instance.pulso.created_by,
            verb='comentou seu pulso',
        )
