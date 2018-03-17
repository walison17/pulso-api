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

    def test_get_all_pulso_participants(self):
        pulso = mommy.make('pulsos.Pulso', created_by=self.user)
        participant_1 = mommy.make('accounts.User')
        participant_2 = mommy.make('accounts.User')
        mommy.make(
            'comments.Comment', pulso=pulso, author=participant_1, _quantity=5
        )
        mommy.make(
            'comments.Comment', pulso=pulso, author=participant_2, _quantity=5
        )
        mommy.make('comments.Comment', pulso=pulso, author=self.user)

        self.assertIn(participant_1, pulso.participants)
        self.assertIn(participant_2, pulso.participants)
        self.assertNotIn(self.user, pulso.participants)
        self.assertEqual(pulso.comments.count(), 11)

    def test_cancel_pulso(self):
        pulso = mommy.make('pulsos.Pulso')
        self.assertTrue(pulso.is_active())
        self.assertFalse(pulso.is_canceled)
        pulso.cancel()
        self.assertTrue(pulso.is_canceled)
        self.assertFalse(pulso.is_active())

    def test_close_pulso(self):
        pulso = mommy.make('pulsos.Pulso')
        self.assertTrue(pulso.is_active())
        self.assertFalse(pulso.is_closed)
        pulso.close()
        self.assertTrue(pulso.is_closed)
        self.assertFalse(pulso.is_active())

    def test_pulso_is_not_active_when_not_happening(self):
        with mock.patch(
            'pulsos.models.timezone.now',
            return_value=datetime.datetime.now() - datetime.timedelta(hours=5)
        ):
            pulso = mommy.make('pulsos.Pulso')
        self.assertFalse(pulso.is_active())
