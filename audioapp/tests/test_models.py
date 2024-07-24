from django.test import TestCase
from django.contrib.auth.models import User
from .factories import UserFactory, AudioFileFactory, CommentFactory
from audioapp.models import Like, Comment


class LikeModelTests(TestCase):

    def test_like_model(self):
        user = UserFactory()
        audio_file = AudioFileFactory(user=user)
        like = Like.objects.create(user=user, audio_file=audio_file)
        self.assertEqual(like.user, user)
        self.assertEqual(like.audio_file, audio_file)


class CommentModelTests(TestCase):

    def test_create_comment(self):
        user = UserFactory()
        audio_file = AudioFileFactory(user=user)
        comment = CommentFactory(
            user=user, audio_file=audio_file, text="This is a test comment."
        )
        self.assertEqual(comment.user, user)
        self.assertEqual(comment.audio_file, audio_file)
        self.assertEqual(comment.text, "This is a test comment.")

    def test_comment_relationships(self):
        user = UserFactory()
        audio_file = AudioFileFactory(user=user)
        comment = CommentFactory(user=user, audio_file=audio_file)
        self.assertIn(comment, audio_file.comments.all())
        self.assertIn(comment, Comment.objects.filter(user=user))
