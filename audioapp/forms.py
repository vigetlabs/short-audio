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
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 5,
                    "cols": 30,  
                    "class": "w-full p-2 border border-gray-300 rounded",
                    "placeholder": "Write your comment here...",
                }
            ),
        }
