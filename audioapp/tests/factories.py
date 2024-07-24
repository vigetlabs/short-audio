import factory
from django.contrib.auth.models import User
from audioapp.models import AudioFile, Like, Comment
from factory.django import DjangoModelFactory
from django.core.files.base import ContentFile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")


class AudioFileFactory(DjangoModelFactory):
    class Meta:
        model = AudioFile

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f"Audio Title {n}")
    description = "This is a test description"
    file = factory.LazyAttribute(
        lambda _: ContentFile(b"Test file content", "test.mp4")
    )


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    audio_file = factory.SubFactory(AudioFileFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    audio_file = factory.SubFactory(AudioFileFactory)
    text = factory.Sequence(lambda n: f"This is comment {n}")
