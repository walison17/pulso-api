from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .serializers import CommentSerializer
from pulsos.models import Pulso


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Pulso.objects.happening()
    lookup_url_kwarg = 'pk'
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        pulso = self.get_object()
        serializer = serializer.save(
            author=self.request.user, pulso=pulso
        )
        super().perform_create(serializer)

    def list(self, request, *args, **kwargs):
        pulso = self.get_object()
        queryset = pulso.comments.all()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
