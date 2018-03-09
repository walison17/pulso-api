from django.dispatch import Signal, receiver


canceled_pulso = Signal(providing_args=['pulso'])
closed_pulso = Signal(providing_args=['pulso'])


@receiver(canceled_pulso)
def notify_users_from_cancellation(sender, pulso, **kwargs):
    pass
