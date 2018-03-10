from rest_framework.test import APITestCase, APISimpleTestCase
from rest_framework import serializers
from django.contrib.gis.geos import Point

from model_mommy import mommy

from ..serializers import PulsoSerializer, LocationSerializer
from ..models import Pulso


class TestPulsoSerializer(APITestCase):

    def setUp(self):
        self.pulso = mommy.make(Pulso)
        lat, long = self.pulso.location.coords
        self.pulso_payload = {
            'created_by': {
                'id': self.pulso.created_by.id,
                'first_name': self.pulso.created_by.first_name,
                'last_name': self.pulso.created_by.last_name,
                'photo_url': self.pulso.created_by.photo_url
            },
            'description': self.pulso.description,
            'radius': self.pulso.radius,
            'created_at': self.pulso.created_at,
            'ends_at': self.pulso.ends_at,
            'location': {
                'lat': lat,
                'long': long
            }
        }

        self.serializer = PulsoSerializer(self.pulso)

    def test_contains_expected_fields(self):
        self.assertEqual(
            self.serializer.data['description'],
            self.pulso_payload['description']
        )

    def test_contains_expected_pulso_creator(self):
        self.assertEqual(
            self.serializer.data['created_by'],
            self.pulso_payload['created_by']
        )

    def test_contains_expected_comments_count(self):
        mommy.make('comments.Comment', pulso=self.pulso, _quantity=10)
        self.assertEqual(
            self.serializer.data['comments_count'], 10
        )

    def test_radius_validation(self):
        invalid_payload = self.pulso_payload.update({'radius': 5})
        with self.assertRaises(serializers.ValidationError):
            serializer = PulsoSerializer(data=invalid_payload)
            serializer.is_valid(raise_exception=True)

    def test_raises_exception_when_user_cannot_create_new_pulso(self):
        user = mommy.make('accounts.User')
        mommy.make(Pulso, created_by=user, _quantity=2)
        with self.assertRaises(serializers.ValidationError):
            serializer = PulsoSerializer(
                data=self.pulso_payload,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=user)


class TestLocationSerializer(APISimpleTestCase):

    def setUp(self):
        self.location = {
            'lat': -8.2777392,
            'long': -35.9716179
        }
        self.serializer = LocationSerializer()

    def test_internal_value(self):
        self.assertIsInstance(
            self.serializer.to_internal_value(self.location),
            Point
        )

    def test_to_representation(self):
        point = Point(*self.location.values())
        result = self.serializer.to_representation(point)
        self.assertEqual(result['lat'], self.location['lat'])
        self.assertEqual(result['long'], self.location['long'])
