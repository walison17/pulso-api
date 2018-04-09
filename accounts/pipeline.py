from django.conf import settings

from .models import User


def create_user(backend, details, response, user=None, *args, **kwargs):
    """Cria um novo usuário com os dados provenientes da api do facebook"""
    if user:
        return {'is_new': False}

    location = response['location']['location']
    user = User.objects.create_user(
        email=response['email'],
        username=response['email'],
        first_name=response['first_name'],
        last_name=response['last_name'],
        photo_url='https://graph.facebook.com/{0}/picture?type=large'.format(
            response['id']
        ),
        password=settings.DEFAULT_USER_PASSWORD,
        gender=response['gender'],
        about=response.get('about', None),
        city=location['city'],
        state=location['state'],
        country=location['country'],
        facebook_id=response['id'],
        facebook_url=response['link'],
        facebook_friends_ids=[friend['id'] for friend in response['friends']['data']],
    )
    return {'is_new': True, 'user': user}


def update_user(backend, response, details, user=None, *args, **kwargs):
    """
    Atualiza os atributos do usuário quando houver divergencias entre os dados
    vindos da Api e os dados já armazenados
    """
    if user:
        location = response['location']['location']
        user.facebook_id = response['id']
        user.first_name = response['first_name']
        user.last_name = response['last_name']
        user.facebook_url = response['link']
        user.city = location['city']
        user.state = location['state']
        user.country = location['country']
        user.facebook_friends_ids = [
            friend['id'] for friend in response['friends']['data']
        ]
        user.save()
