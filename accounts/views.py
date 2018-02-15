import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from requests.exceptions import HTTPError

from social_django.utils import psa

from .models import User
from .serializers import UserSerializer


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

@api_view(['POST'])
@csrf_exempt
@permission_classes((IsAuthenticated,))
def add_friend(request):
    serializer = FriendSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        to_user = get_object_or_404(User, pk=serializer.validated_data['id'])
        Friend.objects.add_friend(request.user, to_user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_204_NO_CONTENT)


