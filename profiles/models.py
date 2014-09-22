from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


# Svaki korisnik treba da ima profil u kome su definisani dodati
# podaci o korisniku (fotografija, biografija itd.). Potrebno je
# razlikovati 3 grupe korisnika:
#   - studente;
#   - poslodavce;
#   - administratore.
# Poslodavci mogu samo objavljivati oglase. Ne mogu se na njih
# javljati niti mogu vidjeti detalje o drugim poslodavcima koji
# su ih objavili.
# Studenti mogu pregledati, objavljivati i javljati se na oglase.
# Takodje mogu vidjeti detalje o poslodavcu (ime i prezime, broj
# telefona, ocjene i dojmove)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)        
    profile_photo = models.ImageField(upload_to='profiles', blank=True)    
    is_student = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.get_full_name()
    
 

# When account is created via social, fire django-allauth signal to populate Django User record.
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
@receiver(user_signed_up)
def user_signed_up_test(request, user, sociallogin=None, **kwargs):
    '''
    When a social account is created successfully and this signal is received,
    django-allauth passes in the sociallogin param, giving access to metadata on the remote account, e.g.:
 
    sociallogin.account.provider  # e.g. 'twitter' 
    sociallogin.account.get_avatar_url()
    sociallogin.account.get_profile_url()
    sociallogin.account.extra_data['screen_name']
 
    See the socialaccount_socialaccount table for more in the 'extra_data' field.
    '''       
 
    profile = Profile(user=user)
    profile.save()
    
    #if sociallogin:
        # Extract first / last names from social nets and store on User record
        #if sociallogin.account.provider == 'twitter':
        #    name = sociallogin.account.extra_data['name']
        #    user.first_name = name.split()[0]
        #    user.last_name = name.split()[1]
 
        #if sociallogin.account.provider == 'facebook':
        #    user.first_name = sociallogin.account.extra_data['first_name']
        #    user.last_name = sociallogin.account.extra_data['last_name']
 
        #if sociallogin.account.provider == 'google':
        #    user.first_name = sociallogin.account.extra_data['given_name']
        #    user.last_name = sociallogin.account.extra_data['family_name']
 
        #user.save()    