from django.conf import settings

from .models import User


def create_user(backend, details, response, user=None, *args, **kwargs):
    """Cria um novo usuário com os dados provenientes da api do facebook"""
    if user:
        return { 'is_new': False }
    default_password = settings.DEFAULT_USER_PASSWORD
    location = response['location']['location']
    user = User.objects.create_user(
        email=response['email'],
        username=response['email'],
        first_name=response['first_name'],
        last_name=response['last_name'],
        photo='https://graph.facebook.com/{0}/picture?type=large'.format(response['id']),
        password=default_password,
        gender=response['gender'],
        about=response.get('about', None),
        city=location['city'],  
        state=location['state'],
        country=location['country'],
    )
    return {
        'is_new': True,
        'user': user
    }


def update_user(backend, response, details, user=None, *args, **kwargs):
    """
    Atualiza os atributos do usuário se houver divergencias entre os dados
    vindos da Api
    """
    pass 

