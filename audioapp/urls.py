from django.urls import include, path
from . import views
from .views import upload_audio, audio_detail, user_detail

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/", include("allauth.urls")),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('upload/', upload_audio, name='upload_audio'),
    path('audio/<int:pk>/', audio_detail, name='audio_detail'),
    path('user/<str:username>/', user_detail, name='user_detail'),
    
]
