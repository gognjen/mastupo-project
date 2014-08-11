# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
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

