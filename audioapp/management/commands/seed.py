from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from audioapp.models import AudioFile
from django.core.files import File
import os
import random


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Deleting old data..."))

        # Delete all existing users and audio files
        User.objects.all().delete()
        AudioFile.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Seeding data..."))

        # Create users
        users = []
        for i in range(10):
            user = User.objects.create_user(
                username=f"user{i}", email=f"user{i}@example.com", password="password"
            )
            users.append(user)

        # Get the sample .mp3 file
        sample_audio_path = os.path.join("audioapp", "sample_audio", "baby_shark.mp3")
        if not os.path.exists(sample_audio_path):
            self.stdout.write(self.style.ERROR("Sample audio file not found."))
            return

        # Create audio files
        for i in range(50):
            user = random.choice(users)
            audio_file = AudioFile(
                user=user,
                title=f"Audio Title {i}",
                description=f"This is a description for audio {i}.",
            )
            # Use the sample .mp3 file
            with open(sample_audio_path, "rb") as f:
                audio_file.file.save(f"audio{i}.mp3", File(f), save=True)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
