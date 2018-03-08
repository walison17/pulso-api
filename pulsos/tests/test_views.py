import datetime
from unittest import mock

from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.gis.geos import Point

from model_mommy import mommy

from ..models import Pulso
from ..views import PulsoListView

SHOPPING_DIFUSORA = Point([-8.2777392, -35.9716179])
ARMAZEM_DA_CRIATIVDADE = Point([-8.238869, -35.980656])


class TestPulsoCreateView(APITestCase):

    def setUp(self):
        user = mommy.make('accounts.User')
        token = mommy.make(Token, user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_new_pulso(self):
        payload = {
            'description': 'descrição do pulso..',
            'location': {
                'lat': -8.278606,
                'long': -35.972933
            },
            'radius': 150
        }

        response = self.client.post('/pulsos/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestPulsoList(APITestCase):

    def setUp(self):
        self.user_location = {
            'lat': -8.278606,
            'long': -35.972933
        }
        self.factory = APIRequestFactory()
        self.view = PulsoListView.as_view()

    def test_retrive_available_pulsos(self):
        mommy.make(
            Pulso,
            location=SHOPPING_DIFUSORA,
            radius=1000,
            _quantity=6
        )
        mommy.make(
            Pulso,
            location=ARMAZEM_DA_CRIATIVDADE,
            radius=50,
            _quantity=5
        )
        request = self.factory.get('/pulsos')
        response = self.view(request, **self.user_location)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 6)

    def test_get_available_pulsos(self):
        mommy.make(
            Pulso,
            location=SHOPPING_DIFUSORA,
            radius=1000,
            _quantity=5
        )
        mommy.make(
            Pulso,
            location=ARMAZEM_DA_CRIATIVDADE,
            radius=50,
            _quantity=10
        )

        response = self.client.get(
            '/pulsos/{}/{}/'.format(*self.user_location.values())
        )

        self.assertEqual(Pulso.objects.count(), 15)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)

    def test_get_only_pulsos_not_expired(self):
        with mock.patch(
            'pulsos.models.timezone.now',
            return_value=datetime.datetime.now() - datetime.timedelta(hours=3)
        ):
            mommy.make(
                Pulso,
                location=SHOPPING_DIFUSORA,
                radius=500,
                _quantity=5
            )
        mommy.make(
            Pulso,
            location=SHOPPING_DIFUSORA,
            radius=500,
            _quantity=5
        )

        response = self.client.get(
            '/pulsos/{}/{}/'.format(*self.user_location.values())
        )

        self.assertEqual(Pulso.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
