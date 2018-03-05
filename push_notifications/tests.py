from unittest.mock import Mock
from contextlib import contextmanager

from django.test import TestCase
from model_mommy import mommy
from notifications.signals import notify

from .signals import user_was_followed
from accounts.models import User


@contextmanager
def catch_signal(signal):
    handler = Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)


class NotificationTest(TestCase):

    def setUp(self):
        self.user = mommy.make('accounts.User', first_name='walison')
        self.other_user = mommy.make('accounts.User', first_name='filipe')

    def test_notify_when_user_was_followed(self):
        self.assertEqual(self.user.following.count(), 0)
        self.assertEqual(self.other_user.followers.count(), 0)

        with catch_signal(user_was_followed) as handler:
            self.user.follow(self.other_user)
            handler.assert_called_once_with(
                sender=User,
                follower=self.user,
                followee=self.other_user,
                signal=user_was_followed
            )

        self.assertEqual(self.user.following.count(), 1)
        self.assertEqual(self.other_user.followers.count(), 1)

    def test_save_notification_on_db_when_following(self):
        self.assertEqual(self.other_user.notifications.count(), 0)

        with catch_signal(notify) as handler:
            self.user.follow(self.other_user)
            handler.assert_called_once_with(
                sender=self.user,
                recipient=self.other_user,
                verb='seguiu você',
                signal=notify,
            )

        self.assertEqual(self.other_user.notifications.count(), 1)
