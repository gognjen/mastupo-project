from django.contrib import admin
from .models import Job, PhoneNumber, JobApplication, ExternalJob

# Register your models here.
admin.site.register(Job)
admin.site.register(PhoneNumber)
admin.site.register(JobApplication)
admin.site.register(ExternalJob)