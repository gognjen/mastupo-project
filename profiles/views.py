from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProfileForm
from .models import Profile
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


def profile(request):
    user = request.user
    if request.POST:
        form = ProfileForm(request.POST)
        
        if form.is_valid():            
            profile = Profile.objects.get(user=request.user)            
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            user.first_name
            profile.save()
            
            messages.success(request, _("Profile details changed successfully."))
            
            return redirect('profile')
    else:        
        form = ProfileForm(initial={'first_name': user.first_name, 'last_name': user.last_name})               
        
    return render(request, 'account/profile.html', { 'form': form, })
    
    