from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Pulso
from .serializers import PulsoSerializer, PulsoWithDistanceSerializer


class PulsoListView(ListAPIView):
    serializer_class = PulsoWithDistanceSerializer

    def get_queryset(self):
        location = {
            'lat': float(self.kwargs['lat']),
            'long': float(self.kwargs['long'])
        }
        return Pulso.objects.available_for(**location)


class PulsoCreateView(CreateAPIView):
    serializer_class = PulsoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer = serializer.save(created_by=self.request.user)
        super().perform_create(serializer)
