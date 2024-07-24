from django.test import TestCase, Client
from django.urls import reverse
from .factories import UserFactory, AudioFileFactory, LikeFactory, CommentFactory
from audioapp.models import AudioFile, Like, Comment


class AudioFileViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username="testuser")
        self.audio_file = AudioFileFactory(user=self.user)
        self.client.login(username="testuser", password="password")

    def test_index_view(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.audio_file.title)

    def test_profile_view_authenticated(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")
        self.assertContains(response, self.audio_file.title)

    def test_profile_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_upload_audio_get(self):
        response = self.client.get(reverse("upload_audio"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "upload_audio.html")

    def test_upload_audio_post(self):
        with open(self.audio_file.file.path, "rb") as file:
            response = self.client.post(
                reverse("upload_audio"),
                {
                    "title": "New Test Audio",
                    "description": "New Description",
                    "file": file,
                },
            )
        if response.status_code == 200:
            print(response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(AudioFile.objects.filter(title="New Test Audio").exists())

    def test_audio_detail_view(self):
        response = self.client.get(reverse("audio_detail", args=[self.audio_file.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "audio_detail.html")
        self.assertContains(response, self.audio_file.title)

    def test_user_detail_view(self):
        response = self.client.get(reverse("user_detail", args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_detail.html")
        self.assertContains(response, self.audio_file.title)

    def test_like_audio(self):
        response = self.client.post(reverse("like_audio", args=[self.audio_file.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Like.objects.filter(user=self.user, audio_file=self.audio_file).exists()
        )

    def test_unlike_audio(self):
        like = LikeFactory(user=self.user, audio_file=self.audio_file)
        response = self.client.post(reverse("unlike_audio", args=[self.audio_file.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Like.objects.filter(user=self.user, audio_file=self.audio_file).exists()
        )

    def test_create_comment(self):
        comment = CommentFactory(
            user=self.user, audio_file=self.audio_file, text="This is a test comment."
        )
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.audio_file, self.audio_file)
        self.assertEqual(comment.text, "This is a test comment.")

    def test_comment_relationships(self):
        comment = CommentFactory(user=self.user, audio_file=self.audio_file)
        self.assertIn(comment, self.audio_file.comments.all())
        self.assertIn(comment, Comment.objects.filter(user=self.user))
