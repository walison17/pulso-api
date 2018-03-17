from contextlib import contextmanager
from unittest.mock import Mock

from rest_framework.test import APITestCase
from model_mommy import mommy
from django.db.models.signals import post_save

from ..signals import canceled_pulso, closed_pulso
from ..models import Pulso
from comments.models import Comment
from notifications.models import Notification


@contextmanager
def catch_signal(signal, sender=None):
    handler = Mock()
    signal.connect(handler, sender=sender)
    yield handler
    signal.disconnect(handler)


class TestPulsoSignals(APITestCase):

    def setUp(self):
        self.pulso = mommy.make(Pulso)

    def test_notify_users_from_cancellation(self):
        with catch_signal(canceled_pulso) as handler:
            comment = mommy.make('comments.Comment', pulso=self.pulso)
            self.pulso.cancel()
            handler.assert_called_once_with(
                sender=Pulso,
                pulso=self.pulso,
                signal=canceled_pulso
            )
        self.assertEqual(
            Notification.objects.filter(recipient=comment.author).count(), 1
        )

    def test_notify_users_about_close(self):
        with catch_signal(closed_pulso) as handler:
            comment = mommy.make('comments.Comment', pulso=self.pulso)
            self.pulso.close()
            handler.assert_called_once_with(
                sender=Pulso,
                pulso=self.pulso,
                signal=closed_pulso
            )
        self.assertEqual(
            Notification.objects.filter(recipient=comment.author).count(), 1
        )

    def test_notify_creator_about_interaction(self):
        with catch_signal(post_save, Comment) as handler:
            comment = mommy.make('comments.Comment', pulso=self.pulso)
            handler.assert_called_once_with(
                sender=Comment,
                instance=comment,
                signal=post_save,
                using='default',
                update_fields=None,
                raw=False,
                created=True
            )
        self.assertEqual(self.pulso.comments.count(), 1)
        self.assertEqual(self.pulso.created_by.notifications.count(), 1)

    def test_shoudnt_notify_creator_when_he_comments_the_pulso(self):
        with catch_signal(post_save, Comment) as handler:
            comment = mommy.make('comments.Comment',
                                 pulso=self.pulso,
                                 author=self.pulso.created_by)
            handler.assert_called_once_with(
                sender=Comment,
                instance=comment,
                signal=post_save,
                using='default',
                update_fields=None,
                raw=False,
                created=True
            )
        self.assertEqual(self.pulso.comments.count(), 1)
        self.assertEqual(self.pulso.created_by.notifications.count(), 0)
