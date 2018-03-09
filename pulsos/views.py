from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     DestroyAPIView, RetrieveAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Pulso
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


class PulsoCancelView(DestroyAPIView):

    def get_queryset(self):
        return Pulso.objects.happening().created_by(self.request.user)

    def perform_destroy(self, instance):
        instance.cancel()


class PulsoCloseView(RetrieveAPIView):

    def get_queryset(self):
        return Pulso.objects.happening().created_by(self.request.user)

    def retrieve(self, requeest, *args, **kwargs):
        instance = self.get_object()
        instance.close()
        return Response(status=status.HTTP_204_NO_CONTENT)
