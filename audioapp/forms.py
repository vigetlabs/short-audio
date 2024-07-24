from django import forms
from .models import AudioFile, Comment


class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ["title", "description", "file"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
