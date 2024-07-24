from django.test import TestCase
from audioapp.forms import CommentForm


class CommentFormTests(TestCase):

    def test_valid_form(self):
        data = {"text": "This is a test comment."}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"text": ""}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
