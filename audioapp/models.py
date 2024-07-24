from django.db import models
from django.contrib.auth.models import User

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    file = models.FileField(upload_to='audio_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def like_count(self):
        return self.like_set.count()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.ForeignKey(AudioFile, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'audio_file')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_file = models.ForeignKey(AudioFile, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
