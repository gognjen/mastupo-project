# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import Job, PhoneNumber

class AddJobForm(forms.ModelForm):    
    description = forms.CharField(label=_('Opis posla'), widget=forms.Textarea())
    price = forms.DecimalField(label=_('Novcana nagrada'), widget=forms.TextInput())
    #workers_needed = forms.IntegerField(label=_('Number of workers'), widget=forms.TextInput())
    address = forms.CharField(label=_('Address'), widget=forms.TextInput())
    class Meta:
        model = Job
        fields = ('description', 'price', 'address',)
              
        
class PhoneNumberForm(forms.ModelForm):
    phone_number = forms.CharField(label=_('Broj telefona'), widget=forms.TextInput())
    class Meta:
        model = PhoneNumber
        fields = ('phone_number',)


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