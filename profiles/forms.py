from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import Profile
from notification import models as notification
from django.contrib.auth.models import User

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30,
                                 label=_('First name'),
                                 widget=forms.TextInput(attrs={'placeholder':_('First name')}))
    last_name = forms.CharField(max_length=30,
                                label=_('Last name'),
                                widget=forms.TextInput(attrs={'placeholder':_('Last name')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']        
        user.save()
        profile = Profile(user=user)
        profile.save()
        #notification.send([User.objects.get(username='ognjen'),], "accounts_register")
        
        

class ProfileForm(forms.ModelForm):    
    first_name = forms.CharField(max_length=30,
                                 label=_('First name'),
                                 widget=forms.TextInput(attrs={'placeholder':_('First name')}))
    last_name = forms.CharField(max_length=30,
                                label=_('Last name'),
                                widget=forms.TextInput(attrs={'placeholder':_('Last name')}))
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name')