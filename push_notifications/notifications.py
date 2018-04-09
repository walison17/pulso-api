from django.conf import settings

import json
import requests

from .models import Device


TITLE = 'Pulso'
ICON = 'notification_icon'
COLOR = '#6f41bf'
SOUND = 'default'


class Notification:
    notification_type = None

    def __init__(self, pulso):
        self.pulso = pulso

    def get_message(self):
        pass

    def get_player_ids(self):
        devices = Device.objects \
            .from_users(self.pulso.participants) \
            .player_ids()
        return list(devices)

    def get_data(self):
        return {
            'notification_type': self.notification_type,
            'object_type': 'PULSO',
            'object_id': self.pulso.pk,
            'icon': ICON,
            'color': COLOR
        }

    def has_filters(self):
        return len(self.get_filters()) > 0

    def get_filters(self):
        return []


class ClosePulsoNotification(Notification):
    notification_type = 'CLOSEMENT'

    def get_message(self):
        return f'{self.pulso.created_by.get_full_name()} correspondeu o pulso.'


class FriendCreatePulsoNotification(Notification):
    notification_type = 'NEW_PULSO'

    def get_message(self):
        return f'{self.pulso.created_by.get_full_name()} está pulsando \
        próximo de você.'

    def get_player_ids(self):
        followers = self.pulso.created_by.followers.all()
        devices = Device.objects \
            .from_users(followers) \
            .player_ids()
        return list(devices)

    def get_filters(self):
        lat, long = self.pulso.location.coords
        return [
            {
                'field': 'location',
                'radius': self.pulso.radius,
                'lat': lat,
                'long': long
            }
        ]


class NewInteractionNotification(Notification):
    notification_type = 'INTERACTION'

    def get_message(self):
        return f'{self.pulso.created_by.get_full_name()} interagiu \
        com seu pulso'

    def get_player_ids(self):
        devices = Device.objects \
            .from_user(self.pulso.created_by) \
            .player_ids()
        return list(devices)


class CancelPulsoNotification(Notification):
    notification_type = 'CANCELLATION'

    def get_message(self):
        return f'{self.pulso.created_by.get_full_name()} cancelou o pulso.'


class OneSignalNotifier:
    BASE_URL = 'https://onesignal.com/api'
    HEADERS = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': f'Basic {settings.ONE_SIGNAL_REST_KEY}'
    }

    def __init__(self, app_id=None):
        self.app_id = app_id or settings.ONE_SIGNAL_APP_ID

    def push(self, notification: Notification):
        payload = {
            'app_id': self.app_id,
            'title': TITLE,
            'large_icon': ICON,
            'contents': {
                'en': notification.get_message()
            },
            'data': notification.get_data(),
            'include_player_ids': notification.get_player_ids()
        }

        if notification.has_filters():
            payload['filters'] = notification.get_filters()

        return requests.post(
            'https://onesignal.com/api/v1/notifications',
            headers=self.HEADERS,
            data=json.dumps(payload)
        )
