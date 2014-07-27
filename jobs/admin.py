from django.contrib import admin
from .models import Job, PhoneNumber, JobApplication

# Register your models here.
admin.site.register(Job)
admin.site.register(PhoneNumber)
admin.site.register(JobApplication)