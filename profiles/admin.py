from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Profile


admin.site.register(Profile)