from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AudioFile
from .forms import AudioFileForm
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

class AudioAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.audio_file = AudioFile.objects.create(
            user=self.user,
            title='Test Audio',
            file=SimpleUploadedFile("file.mp4", b"file_content", content_type="audio/mp4")
        )
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Test Audio')
    
    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'Test Audio')
    
    def test_profile_view_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_upload_audio_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('upload_audio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'upload_audio.html')
    
    def test_upload_audio_post(self):
        self.client.login(username='testuser', password='testpassword')
        with BytesIO(b"file_content") as fp:
            fp.name = 'test.mp4'
            response = self.client.post(reverse('upload_audio'), {
                'title': 'New Test Audio',
                'description': 'Description',
                'file': SimpleUploadedFile(fp.name, fp.read(), content_type='audio/mp4')
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(AudioFile.objects.filter(title='New Test Audio').exists())
    
    def test_audio_detail_view(self):
        response = self.client.get(reverse('audio_detail', args=[self.audio_file.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'audio_detail.html')
        self.assertContains(response, 'Test Audio')
    
    def test_user_detail_view(self):
        response = self.client.get(reverse('user_detail', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_detail.html')
        self.assertContains(response, 'Test Audio')
