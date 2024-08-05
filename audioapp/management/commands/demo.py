from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from audioapp.models import AudioFile
from django.core.files import File
import os
import shutil



class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Deleting old data..."))

        # Delete all existing users and audio files
        User.objects.all().delete()

        audio_files_dir = os.path.join('media/audio_files')
        if os.path.exists(audio_files_dir):
            shutil.rmtree(audio_files_dir)
            os.makedirs(audio_files_dir)  # Recreate the directory
        self.stdout.write(self.style.SUCCESS("All files in audio_files/ directory removed."))
        self.stdout.write(self.style.SUCCESS("Seeding data..."))

        base_path ='audioapp/demo_audios/'
        # Create users
        users = []
        for user_folder in os.listdir(base_path):
            item_path = os.path.join(base_path, user_folder)
            user_name = os.path.basename(item_path)
            user = User.objects.create_user(
                username=user_name, password="password"
            )
            users.append(user)

        #create sounds
        for user in users:
            user_path = os.path.join(base_path, user.username)
            print(user_path)
            for root, dirs, files in os.walk(user_path):
                for file in files:
                    audio_path = os.path.join(user_path, file)
                    title = file[:-4]
                    description = "This is a description for a sound by", user.username
                    audio_file = AudioFile(
                        user=user,
                        title=title,
                        description=description,
                    )
                    with open(audio_path, "rb") as f:
                        audio_file.file.save(file, File(f), save=True)
                    
        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
