import datetime
from unittest import mock, skip

from django.test import TestCase
from django.contrib.gis.geos import Point

from model_mommy import mommy

from ..models import Pulso


class TestPulsoModel(TestCase):

    SHOPPING_DIFUSORA = Point([-8.2777392, -8.2777392])
    ARMAZEM_DA_CRIATIVDADE = Point([-8.238869, -35.980656])

    def setUp(self):
        self.user = mommy.make('accounts.user')

    def test_create_pulso(self):
        pulso = Pulso.objects.create(
            created_by=self.user,
            location=self.SHOPPING_DIFUSORA,
            radius=100,
            description='descrição do pulso..'
        )

        self.assertEqual(Pulso.objects.count(), 1)
        self.assertEqual(pulso.created_by, self.user)

    @mock.patch('pulsos.models.timezone.now')
    def test_should_last_one_hour(self, mock_now):
        mock_now.return_value = datetime.datetime(2018, 11, 15, hour=15)
        pulso = mommy.make(Pulso)

        self.assertEqual(
            pulso.ends_at,
            datetime.datetime(2018, 11, 15, hour=16)
        )

    def test_retrive_only_pulsos_that_are_happening_now(self):
        with mock.patch(
            'pulsos.models.timezone.now',
            return_value=datetime.datetime(2017, 11, 15, hour=15)
        ):
            mommy.make(Pulso, _quantity=2)

        mommy.make(Pulso, _quantity=5)

        self.assertEqual(Pulso.objects.happening().count(), 5)

    @skip('escapando bug do geoDjango')
    def test_retrieve_pulsos_available_in_my_area(self):
        mommy.make(
            Pulso,
            location=self.SHOPPING_DIFUSORA,
            radius=1000,
            _quantity=2
        )
        mommy.make(
            Pulso,
            location=self.ARMAZEM_DA_CRIATIVDADE,
            _quantity=2
        )

        self.assertEqual(Pulso.objects.all().count(), 4)

        available = Pulso.objects.available_for(-8.278606, -35.972933)

        self.assertEqual(available.count(), 2)

    def test_retrive_only_pulsos_created_by_a_specific_user(self):
        mommy.make(Pulso, created_by=self.user, _quantity=5)
        mommy.make(Pulso, _quantity=5)

        self.assertEqual(Pulso.objects.count(), 10)
        self.assertEqual(Pulso.objects.created_by(self.user).count(), 5)
