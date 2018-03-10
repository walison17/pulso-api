from rest_framework import serializers
from django.contrib.gis.geos import Point

from .models import Pulso
from accounts.models import User
from comments.serializers import CommentSerializer


class PulsoCreatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo_url')


class LocationSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        lat, long = obj.coords
        return {
            'lat': lat,
            'long': long
        }

    def to_internal_value(self, data):
        lat = data.get('lat')
        long = data.get('long')
        return Point([lat, long])


class PulsoSerializer(serializers.ModelSerializer):
    created_by = PulsoCreatorSerializer(read_only=True)
    location = LocationSerializer(write_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    comments_count = serializers.IntegerField(read_only=True,
                                              source='comments.count')

    class Meta:
        model = Pulso
        fields = (
            'id', 'created_by', 'description', 'radius',
            'created_at', 'ends_at', 'location', 'comments_count',
            'comments',
        )
        read_only_fields = (
            'created_by', 'ends_at', 'created_at',
        )

    def validate_radius(self, value):
        if not value >= 25 or not value <= 1000:
            raise serializers.ValidationError(
                'Distãncia deve ser entre 25 e 1000 metros.'
            )
        return value

    def create(self, validated_data):
        if Pulso.objects.happening() \
            .created_by(validated_data['created_by']) \
                .exists():
            raise serializers.ValidationError(
                'Usuário não pode criar pulsos simultâneamente.'
            )
        return Pulso.objects.create(**validated_data)


class PulsoWithDistanceSerializer(PulsoSerializer):
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return obj.distance.m

    class Meta(PulsoSerializer.Meta):
        fields = PulsoSerializer.Meta.fields + ('distance',)
