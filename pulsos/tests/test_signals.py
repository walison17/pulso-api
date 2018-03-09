from contextlib import contextmanager
from unittest.mock import Mock

from rest_framework.test import APITestCase
from model_mommy import mommy

from ..signals import canceled_pulso
from ..models import Pulso


@contextmanager
def catch_signal(signal):
    handler = Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)


class TestPulsoSignals(APITestCase):

    def setUp(self):
        self.pulso = mommy.make(Pulso)

    def test_notify_users_from_cancellation(self):
        with catch_signal(canceled_pulso) as handler:
            self.pulso.cancel()
            handler.assert_called_once_with(
                sender=Pulso,
                pulso=self.pulso,
                signal=canceled_pulso
            )
