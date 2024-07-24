from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import allauth
from .forms import AudioFileForm, CommentForm
from .models import AudioFile, Like, Comment
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
            return redirect(reverse('audio_detail', args=[audio_file.pk]))
    else:
        form = AudioFileForm()
    return render(request, 'upload_audio.html', {'form': form})

def audio_detail(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    comments = audio_file.comments.all()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, audio_file=audio_file).exists()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.audio_file = audio_file
            comment.save()
            return redirect('audio_detail', pk=audio_file.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'audio_detail.html', {
        'audio_file': audio_file,
        'user_liked': user_liked,
        'comments': comments,
        'comment_form': comment_form,
    })

def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    audio_files = AudioFile.objects.filter(user=user)
    return render(request, 'user_detail.html', {'user': user, 'audio_files': audio_files})

@login_required
def like_audio(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, audio_file=audio_file)
    return redirect('audio_detail', pk=audio_file.pk)

@login_required
def unlike_audio(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    Like.objects.filter(user=request.user, audio_file=audio_file).delete()
    return redirect('audio_detail', pk=audio_file.pk)
    
