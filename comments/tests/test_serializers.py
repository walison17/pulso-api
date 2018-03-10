from rest_framework.test import APITestCase

from model_mommy import mommy

from ..models import Comment
from ..serializers import CommentSerializer

PAYLOAD = {
    'text': 'meu comentário'
}


class TestCommentSerializer(APITestCase):

    def setUp(self):
        self.comment = mommy.make(Comment)

    def test_contains_expected_fields(self):
        serializer = CommentSerializer(instance=self.comment)

        self.assertEqual(serializer.data['id'], self.comment.id)

    def test_deserialize_and_create_comment(self):
        pulso = mommy.make('pulsos.Pulso')
        author = mommy.make('accounts.User')
        serializer = CommentSerializer(data=PAYLOAD)
        serializer.is_valid()
        instance = serializer.save(author=author, pulso=pulso)

        self.assertIsInstance(instance, Comment)
