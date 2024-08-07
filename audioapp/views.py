from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import allauth, random
from .forms import AudioFileForm, CommentForm
from .models import AudioFile, Like, Comment
from django.contrib.auth.models import User
from django.db.models import Subquery




@login_required
def upload_audio(request):
    if request.method == "POST":
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = form.save(commit=False)
            audio_file.user = request.user
            audio_file.save()
            if "fyp_order" in request.session:
                request.session["fyp_order"].append(audio_file.id)
                request.session.modified = True
            return redirect(reverse("audio_detail", args=[audio_file.pk]))
    else:
        form = AudioFileForm()
    return render(request, "upload_audio.html", {"form": form})


def audio_detail(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    comments = audio_file.comments.all()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(
            user=request.user, audio_file=audio_file
        ).exists()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.audio_file = audio_file
            comment.save()
            return redirect("audio_detail", pk=audio_file.pk)
    else:
        comment_form = CommentForm()

    return render(
        request,
        "audio_detail.html",
        {
            "audio_file": audio_file,
            "user_liked": user_liked,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


def user_detail(request, username):
    page_user = get_object_or_404(User, username=username)
    audio_files = AudioFile.objects.filter(user=page_user)
    all_liked_sounds = Like.objects.filter(user=page_user).values('audio_file_id')
    user_liked_sounds = AudioFile.objects.filter(id__in=Subquery(all_liked_sounds))
    return render(
        request,
        "user_detail.html",
        {"page_user": page_user, "audio_files": audio_files, "user_liked_sounds": user_liked_sounds},
    )


@login_required
def like_audio(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    Like.objects.get_or_create(user=request.user, audio_file=audio_file)
    return redirect("audio_detail", pk=audio_file.pk)


@login_required
def unlike_audio(request, pk):
    audio_file = get_object_or_404(AudioFile, pk=pk)
    Like.objects.filter(user=request.user, audio_file=audio_file).delete()
    return redirect("audio_detail", pk=audio_file.pk)


@login_required
def for_you(request):
    def update_fyp_index(request, fyp_order, fyp_index):
        reached_end = False
        action = request.GET.get("action")

        if action == "next" and fyp_index < len(fyp_order) - 1:
            fyp_index += 1
            reached_end = fyp_index == len(fyp_order) - 1
        elif action == "previous" and fyp_index > 0:
            fyp_index -= 1

        request.session["fyp_index"] = fyp_index
        request.session.modified = True

        return fyp_index, reached_end

    def handle_post_request(request, audio_file):
        action = request.POST.get("action")
        if action == "comment":
            handle_comment(request, audio_file)
        elif action == "like":
            handle_like(request, audio_file)

    def handle_comment(request, audio_file):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.audio_file = audio_file
            comment.save()

    def handle_like(request, audio_file):
        if has_liked(request, audio_file):
            Like.objects.filter(user=request.user, audio_file=audio_file).delete()
        else:
            like, created = Like.objects.get_or_create(
                user=request.user, audio_file=audio_file
            )
            if created:
                print("Like created:", like)
            

    def has_liked(request, audio_file):
        return Like.objects.filter(user=request.user, audio_file=audio_file).exists()

    def fyp_xml_http_request(audio_file, reached_end, fyp_index, request):
        return JsonResponse(
            {
                "audio_file_url": audio_file.file.url,
                "title": audio_file.title,
                "description": audio_file.description,
                "fyp_index": fyp_index,
                "reached_end": reached_end,
                "has_liked": has_liked(request, audio_file),
                "username": audio_file.user.username,
                "like_count": audio_file.like_set.count(),
                "profile_url": reverse("user_detail", args=[audio_file.user.username]),
                "audio_source": audio_file.file.url,
                "comments": [
                    {
                        "user": comment.user.username,
                        "text": comment.text,
                        "profile_url": reverse(
                            "user_detail", args=[comment.user.username]
                        ),
                    }
                    for comment in audio_file.comments.all()
                ],
            }
        )

    if "fyp_order" not in request.session:
        audio_files = list(AudioFile.objects.all())
        fyp_order = [audio_file.id for audio_file in audio_files]
        random.shuffle(fyp_order)
        request.session["fyp_order"] = fyp_order
        request.session["fyp_index"] = 0

    fyp_order = request.session["fyp_order"]
    fyp_index = request.session["fyp_index"]
    reached_end = fyp_index == len(fyp_order) - 1
    audio_file = get_object_or_404(AudioFile, id=fyp_order[fyp_index])

    if request.method == "POST":
        handle_post_request(request, audio_file)

    if "action" in request.GET:
        fyp_index, reached_end = update_fyp_index(request, fyp_order, fyp_index)

    audio_file = get_object_or_404(AudioFile, id=fyp_order[fyp_index])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return fyp_xml_http_request(audio_file, reached_end, fyp_index, request)

    autoplay = request.session.get("autoplay", False)

    return render(
        request,
        "for_you.html",
        {
            "audio_file": audio_file,
            "fyp_index": fyp_index,
            "reached_end": reached_end,
            "autoplay": autoplay,
            "comment_form": CommentForm(),
            "comments": audio_file.comments.all(),
            "has_liked": has_liked(request, audio_file),
        },
    )


def update_autoplay(request):
    if (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        and "autoplay" in request.GET
    ):
        request.session["autoplay"] = request.GET.get("autoplay") == "true"
        request.session.modified = True
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)
