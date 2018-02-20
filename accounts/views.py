import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank 

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view, permission_classes, authentication_classes
)
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import mixins
from rest_framework.decorators import detail_route, list_route

from requests.exceptions import HTTPError

from social_django.utils import psa

from .models import User
from .serializers import UserSerializer
from relationships.serializers import FolloweeSerializer


class SocialSerializer(serializers.Serializer):
    access_token = serializers.CharField(allow_blank=False)


@psa()
@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def get_token(request, backend):
    serializer = SocialSerializer(data=request.GET)
    if serializer.is_valid(raise_exception=True):
        try:
            access_token = request.GET.get('access_token', None)
            user = request.backend.do_auth(access_token)
        except HTTPError as e: 
            return Response(
                {
                    'errors': {
                        'message': 'token inválido'
                    }
                },
                status.HTTP_400_BAD_REQUEST 
            )
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({ 'token': str(token) })


@api_view(['GET', 'PUT'])
@permission_classes((IsAuthenticated,))
def me(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    if request.method == 'PUT':
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

@api_view(['PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


    @detail_route(methods=['get'], url_path='following')
    def friends(self, request, pk=None):
        """Busca os amigos (usuários seguidos) pelo usuário com o id informado"""
        user = self.get_object()
        friends = user.following.all()

        page = self.paginate_queryset(friends)
        if page is not None:
            serializer = FolloweeSerializer(friends, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FolloweeSerializer(friends, many=True)
        return Response(serializer.data)


    
    @list_route(methods=['get'], url_path='search')
    def search_user(self, request):
        vector = SearchVector('first_name', weight='A') + SearchVector('last_name', weight='B') + SearchVector('city', weight='C')
        query = SearchQuery(request.GET.get('q', None))
        search_result = User.objects \
            .annotate(rank=SearchRank(vector, query)) \
            .order_by('-rank')

        page = self.paginate_queryset(search_result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(search_result, many=True)
        return self.get_paginated_response(serializer.data)