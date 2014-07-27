from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.job_list, name="job_list"),                       
    url(r'^add_job/$', views.add_job, name="add_job"),
    url(r'^my_jobs/$', views.my_jobs, name="my_jobs"),
    url(r'^(?P<job_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<job_id>[0-9]+)/apply/$', views.apply_for_job, name='apply_for_job'),
    url(r'^(?P<job_id>[0-9]+)/cancel/$', views.cancel_job_application, name='cancel_job_application'),
)
