from rest_framework.test import APITestCase

from model_mommy import mommy

from ..models import User
from ..serializers import AuthUserSerializer


PAYLOAD = {
    'first_name': 'walison',
    'last_name': 'filipe',
    'about': 'descrição..',
    'email': 'walisonfilipe@hotmail.com',
    'password': 'senha_super_segura',
    'city': 'caruaru',
    'state': 'pe',
    'country': 'Brasil',
    'photo_url': 'foto_perfil.jpeg',
    'facebook_url': 'facebook.com/walison.filipe',
}


class TestAccountSerializer(APITestCase):

    def setUp(self):
        self.user = mommy.make(
            User, first_name='walison', last_name='mendes', make_m2m=True
        )

    def test_contains_expected_number_of_created_pulsos(self):
        mommy.make('pulsos.Pulso', created_by=self.user, _quantity=15)
        serializer = AuthUserSerializer(self.user)

        self.assertEqual(serializer.data['created_pulsos_count'], 15)

    def test_contains_expected_number_of_participated_pulsos(self):
        serializer = AuthUserSerializer(self.user)

        self.assertEqual(serializer.data['participated_pulsos_count'], 0)
