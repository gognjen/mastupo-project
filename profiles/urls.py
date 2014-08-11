from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',        
    url(r'^profile/$', views.profile, name="profile"),    
)