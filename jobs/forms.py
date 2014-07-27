from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .models import Job, PhoneNumber

class AddJobForm(forms.ModelForm):    
    description = forms.CharField(label=_('Description'), widget=forms.Textarea(attrs={'placeholder':_('Description')}))
    price = forms.DecimalField(label=_('Price'), widget=forms.TextInput(attrs={'placeholder':_('Price')}))
    workers_needed = forms.IntegerField(label=_('Number of workers'), widget=forms.TextInput(attrs={'placeholder': _('Number of workers')}))
    address = forms.CharField(label=_('Address'), widget=forms.TextInput(attrs={'placeholder':_('Address')}))
    class Meta:
        model = Job
        fields = ('description', 'price', 'workers_needed', 'address',)
        
        
class PhoneNumberForm(forms.ModelForm):
    phone_number = forms.CharField(label=_('Phone number'), widget=forms.TextInput(attrs={'placeholder':_('Phone number')}))
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