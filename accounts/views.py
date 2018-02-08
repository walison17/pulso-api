import json

from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from requests.exceptions import HTTPError

from social_django.utils import psa

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


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieve_authenticated_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
    