from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',        
    url(r'^add-job/$', views.add_job, name="add_job"),
    url(r'^my-jobs/$', views.my_jobs, name="my_jobs"),
    url(r'^external-jobs/$', views.external_jobs, name="external_jobs"),
    url(r'^external-jobs/(?P<job_id>[0-9]+)/$', views.external_detail, name='external_detail'),
    url(r'^(?P<job_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<job_id>[0-9]+)/edit/$', views.job_edit, name='edit'),
    url(r'^(?P<job_id>[0-9]+)/delete/$', views.job_delete, name='delete'),
    url(r'^(?P<job_id>[0-9]+)/apply/$', views.apply_for_job, name='apply_for_job'),
    url(r'^(?P<job_id>[0-9]+)/cancel/$', views.cancel_job_application, name='cancel_job_application'),
)
