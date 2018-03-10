from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

from model_mommy import mommy

from ..models import Comment

COMMENT_PAYLOAD = {
    'text': 'comentário..'
}


class AuthenticatedMixin:

    def setUp(self):
        self.user = mommy.make('accounts.User')
        self.pulso = mommy.make('pulsos.Pulso')
        token = mommy.make(Token, user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')


class TestCommentCreateView(AuthenticatedMixin, APITestCase):

    def test_create_comment(self):
        response = self.client.post(
            '/pulsos/{pulso_id}/comments/'.format(
                pulso_id=self.pulso.pk
            ),
            data=COMMENT_PAYLOAD,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.posted_on(self.pulso).count(), 1)
        self.assertEqual(Comment.objects.created_by(self.user).count(), 1)

    def test_thown_error_when_post_comment_on_canceled_pulso(self):
        canceled_pulso = mommy.make('pulsos.Pulso', is_canceled=True)
        response = self.client.post(
            '/pulsos/{pulso_id}/comments/'.format(
                pulso_id=canceled_pulso.pk
            ),
            data=COMMENT_PAYLOAD,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.created_by(self.user).count(), 0)

    def test_throw_404_when_post_comment_on_closed_pulso(self):
        closed_pulso = mommy.make('pulsos.Pulso', is_closed=True)
        response = self.client.post(
            '/pulsos/{pulso_id}/comments/'.format(
                pulso_id=closed_pulso.pk
            ),
            data=COMMENT_PAYLOAD,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Comment.objects.created_by(self.user).count(), 0),

    def test_throw_validation_error_when_send_blank_message(self):
        response = self.client.post(
            '/pulsos/{pulso_id}/comments/'.format(
                pulso_id=self.pulso.pk
            ),
            data={'text': ''},
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.posted_on(self.pulso).count(), 0)
        self.assertEqual(Comment.objects.created_by(self.user).count(), 0)


class TestCommentListView(AuthenticatedMixin, APITestCase):

    def test_list_all_comments_from_pulso(self):
        mommy.make(Comment, pulso=self.pulso, _quantity=10)
        response = self.client.get(
            '/pulsos/{pulso_id}/comments/'.format(pulso_id=self.pulso.pk)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 10)

    def test_throw_404_on_get_comments_from_canceled_pulso(self):
        canceled_pulso = mommy.make('pulsos.Pulso', is_canceled=True)
        response = self.client.get(
            '/pulsos/{pulso_id}/comments/'.format(
                pulso_id=canceled_pulso.pk
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
