from rest_framework.test import APITestCase

from model_mommy import mommy

from ..models import Comment


class TestCommentModels(APITestCase):

    def setUp(self):
        self.user = mommy.make('accounts.User')
        self.pulso = mommy.make('pulsos.Pulso')

    def test_get_all_comments_from_pulso(self):
        mommy.make(Comment, pulso=self.pulso, _quantity=10)
        mommy.make(Comment, _quantity=5)

        self.assertEqual(Comment.objects.count(), 15)
        self.assertEqual(Comment.objects.posted_on(self.pulso).count(), 10)

    def test_get_all_comments_from_user(self):
        mommy.make(Comment, author=self.user, _quantity=5)
        mommy.make(Comment, _quantity=10)

        self.assertEqual(Comment.objects.count(), 15)
        self.assertEqual(Comment.objects.created_by(self.user).count(), 5)

    def test_get_all_comments_from_user_on_specific_pulso(self):
        other_pulso = mommy.make('pulsos.Pulso')
        mommy.make(Comment, pulso=other_pulso, _quantity=10)

        mommy.make(Comment, pulso=self.pulso, author=self.user, _quantity=5)

        self.assertEqual(Comment.objects.count(), 15)
        self.assertEqual(Comment.objects.posted_on(other_pulso).count(), 10)
        self.assertEqual(
            Comment.objects.posted_on(self.pulso).created_by(self.user).count(), 5
        )
