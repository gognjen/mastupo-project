from django.db import models
from django.conf import settings

        
class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=15)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    primary = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.phone_number
    
       
class Job(models.Model):    
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    phone_number = models.ForeignKey(PhoneNumber)
    status = models.CharField(max_length=30)    
    address = models.CharField(max_length=100)
    
    def user_applied(self, user):
        return self.jobapplication_set.filter(user=user).count() > 0
    
    def available(self, ):
        return self.jobapplication_set.count() < self.workers_needed    
    
    def __unicode__(self):
        return self.description
    

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    job = models.ForeignKey(Job)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user.get_full_name() + "'s application"
    