from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'event_subscribe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$', 'subscribe.views.index', name='index'), 
    url(r'^iscrizione-laboratori/', 'subscribe.views.subscribe', name='subscribe'), 

    url(r'^admin/', include(admin.site.urls)),
)
