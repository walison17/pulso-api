from unittest.mock import Mock, patch
from contextlib import contextmanager

from django.test import TestCase
from model_mommy import mommy

from .signals import user_was_followed, notify_new_follower
from accounts.models import User


@contextmanager
def catch_signal(signal):
    handler = Mock()
    signal.connect(handler)
    yield handler 
    signal.disconnect(handler)


class NotificationTest(TestCase):
 
    def setUp(self):
        self.user = mommy.make('accounts.User')
        self.other_user = mommy.make('accounts.User')

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

