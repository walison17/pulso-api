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
        self.user = mommy.make('accounts.User')
        token = mommy.make(Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        self.payload = {
            'description': 'descrição do pulso..',
            'location': {
                'lat': -8.278606,
                'long': -35.972933
            },
            'radius': 150
        }

    def test_create_new_pulso(self):
        response = self.client.post('/pulsos/', self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validation_error_when_create_simultaneous_pulsos(self):
        response_from_first_creation = self.client.post(
            '/pulsos/', self.payload, format='json'
        )

        self.assertEqual(response_from_first_creation.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(Pulso.objects.created_by(self.user).count(), 1)

        response_from_second_creation = self.client.post(
            '/pulsos/', self.payload, format='json'
        )

        self.assertEqual(response_from_second_creation.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Pulso.objects.created_by(self.user).count(), 1)


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


class TestCancelAndCloseView(APITestCase):

    def setUp(self):
        self.user = mommy.make('accounts.User')
        token = mommy.make(Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_cancel_pulso(self):
        created_pulso = mommy.make(Pulso, created_by=self.user)

        self.assertEqual(Pulso.objects.created_by(self.user).count(), 1)

        response = self.client.delete(
            '/pulsos/{pulso_id}/'.format(pulso_id=created_pulso.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Pulso.objects.created_by(self.user).count(), 1)
        self.assertEqual(
            Pulso.objects.canceled().created_by(self.user).count(), 1
        )

    def test_throw_error_when_try_to_canel_a_pulso_from_another_user(self):
        pulso_from_another_user = mommy.make(Pulso)

        self.assertEqual(Pulso.objects.created_by(self.user).count(), 0)
        self.assertEqual(Pulso.objects.count(), 1)

        response = self.client.delete(
            '/pulsos/{pulso_id}/'.format(pulso_id=pulso_from_another_user.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
