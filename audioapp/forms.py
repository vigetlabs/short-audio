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
                    "rows": 5,  # Number of rows
                    "cols": 30,  # Number of columns
                    "class": "w-full p-2 border border-gray-300 rounded",  # Tailwind CSS classes
                    "placeholder": "Write your comment here...",
                }
            ),
        }
