from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     RetrieveAPIView, DestroyAPIView,
                                     RetrieveDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404

from .models import Pulso, DEFAULT_SRID
from .serializers import PulsoSerializer, PulsoWithDistanceSerializer


class PulsoListView(ListAPIView):
    serializer_class = PulsoWithDistanceSerializer

    def get_queryset(self):
        location = {
            'lat': float(self.kwargs['lat']),
            'long': float(self.kwargs['long'])
        }
        return Pulso.objects.happening().available_for(**location)


class PulsoCreateView(CreateAPIView):
    serializer_class = PulsoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer = serializer.save(created_by=self.request.user)
        super().perform_create(serializer)


class PulsoCloseView(RetrieveAPIView):

    def get_queryset(self):
        return Pulso.objects.happening().created_by(self.request.user)

    def retrieve(self, requeest, *args, **kwargs):
        instance = self.get_object()
        instance.close()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PulsoDetailCancelView(RetrieveDestroyAPIView):
    serializer_class = PulsoWithDistanceSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return Pulso.objects.all()
        return Pulso.objects.happening().created_by(self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if 'coords' in self.request.query_params:
            lat, long = self.request.query_params['coords'].split(',')
            current_location = Point(
                float(lat), float(long), srid=DEFAULT_SRID
            )
            queryset = self.get_queryset().annotate(
                distance=Distance('location', current_location)
            )
        return get_object_or_404(queryset, pk=self.kwargs['pk'])

    def perform_destroy(self, instance):
        instance.cancel()
