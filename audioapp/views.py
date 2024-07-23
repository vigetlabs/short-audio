from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import allauth

# Create your views here.
def index(request):
    return render(request, 'index.html')
@login_required

def profile_view(request):
    return render(request, 'profile.html', {'username': request.user.username})


