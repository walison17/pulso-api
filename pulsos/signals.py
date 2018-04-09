from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

from notifications.signals import notify
from comments.models import Comment
from push_notifications import notifications


canceled_pulso = Signal(providing_args=['pulso'])
closed_pulso = Signal(providing_args=['pulso'])
new_pulso_interaction = Signal(providing_args=['pulso', 'author'])


notifier = notifications.OneSignalNotifier()


@receiver(closed_pulso)
def notify_users_about_closement(sender, pulso, **kwargs):
    notification = notifications.ClosePulsoNotification(pulso)
    notifier.push(notification)


@receiver(closed_pulso)
def save_closement_on_db(sender, pulso, **kwargs):
    for p in pulso.participants:
        notify.send(sender=pulso.created_by, recipient=p, verb='correspondeu o pulso.')


@receiver(canceled_pulso)
def notify_users_about_cancellation(sender, pulso, **kwargs):
    notification = notifications.CancelPulsoNotification(pulso)
    notifier.push(notification)


@receiver(canceled_pulso)
def save_cancellation_on_db(sender, pulso, **kwargs):
    for p in pulso.participants:
        notify.send(sender=pulso.created_by, recipient=p, verb='cancelou o pulso.')


@receiver(post_save, sender=Comment)
def notify_creator_about_new_interaction(sender, instance, **kwargs):
    notification = notifications.NewInteractionNotification(instance.pulso)
    notifier.push(notification)


@receiver(post_save, sender=Comment)
def save_interaction_on_db(sender, instance, **kwargs):
    pulso_creator = instance.pulso.created_by
    if pulso_creator != instance.author:
        notify.send(
            sender=instance.author,
            recipient=instance.pulso.created_by,
            verb='comentou seu pulso',
        )
