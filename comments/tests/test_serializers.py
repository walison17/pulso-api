from rest_framework.test import APITestCase

from model_mommy import mommy

from ..models import Comment
from ..serializers import CommentSerializer, AuthorSerializer

PAYLOAD = {
    'text': 'meu comentário'
}


class TestCommentSerializer(APITestCase):

    def setUp(self):
        self.comment = mommy.make(Comment)

    def test_contains_expected_fields(self):
        serializer = CommentSerializer(instance=self.comment)

        self.assertEqual(serializer.data['id'], self.comment.id)
        self.assertEqual(serializer.data['text'], self.comment.text)
        self.assertEqual(
            serializer.data['author'], {
                'id': self.comment.author.id,
                'first_name': self.comment.author.first_name,
                'last_name': self.comment.author.last_name,
                'photo_url': self.comment.author.photo_url
            }
        )

    def test_deserialize_and_create_comment(self):
        pulso = mommy.make('pulsos.Pulso')
        author = mommy.make('accounts.User')
        serializer = CommentSerializer(data=PAYLOAD)
        serializer.is_valid()
        instance = serializer.save(author=author, pulso=pulso)

        self.assertIsInstance(instance, Comment)


class TestAuthorSerializer(APITestCase):

    def setUp(self):
        self.author = mommy.make('accounts.User')

    def test_contains_expected_fields(self):
        serializer = AuthorSerializer(self.author)

        self.assertEqual(serializer.data['id'], self.author.id)
        self.assertEqual(serializer.data['first_name'], self.author.first_name)
        self.assertEqual(serializer.data['last_name'], self.author.last_name)
        self.assertEqual(serializer.data['photo_url'], self.author.photo_url)
