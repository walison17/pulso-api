from django.db import models
from django.conf import settings
from django.utils import timezone
from django.dispatch import Signal
from django.core.exceptions import ValidationError


class Follow(models.Model):
    from_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_followers',
    )
    to_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='%(class)s_following',
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def save(self, *args, **kwargs):
        if self.from_user == self.to_user:
            raise ValidationError('O usuário não pode seguir ele mesmo.')

        super(Follow, self).save(*args, **kwargs)


new_follower = Signal(providing_args=['follower', 'followee'])
