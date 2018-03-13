import datetime

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import F
from django.contrib.gis.db.models.functions import Distance
from django.conf import settings
from django.utils import timezone

from .signals import canceled_pulso, closed_pulso

DEFAULT_SRID = 4326


class PulsoQueryset(models.QuerySet):

    def created_by(self, user):
        return self.filter(created_by=user)

    def happening(self):
        return self.filter(ends_at__gte=timezone.now(),
                           is_closed=False, is_canceled=False)

    def available_for(self, lat, long):
        current_user_location = Point(lat, long, srid=DEFAULT_SRID)
        return self.annotate(
            distance=Distance('location', current_user_location)
        ).filter(distance__lte=F('radius')).order_by('-distance')

    def canceled(self):
        return self.filter(is_canceled=True)

    def closed(self):
        return self.filter(is_closed=True)

    def open(self):
        return self.filter(is_closed=False)


class Pulso(models.Model):
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pulsos'
    )
    description = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField()
    location = models.PointField()
    radius = models.IntegerField(
        default=10, help_text='distância em metros'
    )
    is_closed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    objects = PulsoQueryset.as_manager()

    class Meta:
        ordering = ['ends_at']

    def save(self, *args, **kwargs):
        self.ends_at = timezone.now() + datetime.timedelta(hours=1)
        super(Pulso, self).save(*args, **kwargs)

    def cancel(self):
        self.is_canceled = True
        self.save()
        canceled_pulso.send(sender=self.__class__, pulso=self)

    def close(self):
        self.is_closed = True
        self.save()
        closed_pulso.send(sender=self.__class__, pulso=self)
