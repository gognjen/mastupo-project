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
    address = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    phone_number = models.ForeignKey(PhoneNumber)    
    status = models.CharField(max_length=30)    
    user = models.ForeignKey(settings.AUTH_USER_MODEL)    
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)               
    parent_id = models.IntegerField(default=0)
    
    def user_applied(self, user):
        return self.jobapplication_set.filter(user=user).count() > 0
    
    def available(self, ):
        return self.jobapplication_set.count() == 0    
    
    def __unicode__(self):
        return self.description
    
    
class ExternalJob(models.Model):
    source = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    link = models.URLField()
    date_published = models.DateField()
    date_expire = models.DateField()
    location = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title        

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    job = models.ForeignKey(Job)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user.get_full_name() + "'s application"
    