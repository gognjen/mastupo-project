from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mastupo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'jobs.views.home', name="home"),    
    url(r'^jobs/', include('jobs.urls', namespace="jobs")),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

from . import settings
urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )