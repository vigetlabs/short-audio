from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import allauth
from .forms import AudioFileForm
from .models import AudioFile
from django.contrib.auth.models import User



# Create your views here.
def index(request):
    audio_files = AudioFile.objects.all()
    return render(request, 'index.html', {'audio_files': audio_files})

@login_required
def profile_view(request):
    audio_files = AudioFile.objects.filter(user=request.user)
    context = {
        'username': request.user.username,
        'audio_files': audio_files,
    }
    return render(request, 'profile.html', context)

@login_required
def upload_audio(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save(commit=False)
            audio_file.user = request.user
            audio_file.save()
            return redirect(reverse('profile'))
    else:
        form = AudioFileForm()
    return render(request, 'upload_audio.html', {'form': form})

def audio_detail(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    return render(request, 'audio_detail.html', {'audio_file': audio_file})

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    audio_files = AudioFile.objects.filter(user=user)
    return render(request, 'user_detail.html', {'user': user, 'audio_files': audio_files})

    
