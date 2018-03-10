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

    def test_get_all_interacted_pulsos(self):
        pulso1 = mommy.make('pulsos.Pulso')
        pulso2 = mommy.make('pulsos.Pulso')
        mommy.make(
            'comments.Comment',
            pulso=pulso1,
            author=self.user,
            _quantity=5
        )
        mommy.make(
            'comments.Comment',
            pulso=pulso2,
            author=self.user,
            _quantity=5
        )

        self.assertEqual(self.user.participated_pulsos.count(), 2)
        self.assertEqual(self.user.comments.count(), 10)
