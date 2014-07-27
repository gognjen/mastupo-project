from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def profile(request):
    return render(request, 'profiles/profile.html')