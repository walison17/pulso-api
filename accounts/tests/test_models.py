from rest_framework.test import APITestCase

from model_mommy import mommy

from ..models import User


class TestAccountModels(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)

    def test_get_all_created_pulsos_without_canceled(self):
        mommy.make('pulsos.Pulso', created_by=self.user, _quantity=10)
        pulsos_to_cancell = self.user.pulsos.all()[:5]
        for pulso in pulsos_to_cancell:
            pulso.cancel()

        self.assertEqual(self.user.pulsos.count(), 10)
        self.assertEqual(self.user.created_pulsos.count(), 5)
