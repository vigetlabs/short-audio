from django.urls import include, path
from . import views
from .views import (
    upload_audio,
    audio_detail,
    user_detail,
    like_audio,
    unlike_audio,
    for_you,
    update_autoplay,
)


urlpatterns = [
    path("", for_you, name="for_you"),
    path("accounts/", include("allauth.urls")),
    path("upload/", upload_audio, name="upload_audio"),
    path("audio/<int:pk>/", audio_detail, name="audio_detail"),
    path("user/<str:username>/", user_detail, name="user_detail"),
    path("audio/<int:pk>/like/", like_audio, name="like_audio"),
    path("audio/<int:pk>/unlike/", unlike_audio, name="unlike_audio"),
    path("for_you/", for_you, name="for_you"),
    path("update_autoplay/", update_autoplay, name="update_autoplay"),
]
