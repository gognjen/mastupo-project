from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm


def profile(request):
    profile = request.user
    if request.POST:
        form = ProfileForm(request.POST)
        
        if form.is_valid():
            job = form.save()            
            return redirect('profile')
    else:                       
        form = ProfileForm(initial={'first_name': profile.first_name, 'last_name': profile.last_name})               
        
    return render(request, 'account/profile.html', { 'form': form, })
    
    