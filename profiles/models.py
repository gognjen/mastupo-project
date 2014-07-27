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
    

    