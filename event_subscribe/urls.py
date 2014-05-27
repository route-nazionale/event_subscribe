from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'event_subscribe.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # user interface views
    url(r'^$', 'subscribe.views.index', name='index'),
    url(r'^iscrizione-laboratori/', 'subscribe.views.subscribe', name='subscribe'),
    url(r'^scelta-laboratori/', 'subscribe.views.choose', name='choose'),
    url(r'^logout/', 'subscribe.views.logout', name='logout'),

    # API views
    url(r'^events/', 'base.views.events', name='events'),
    url(r'^event/(?P<event_code>\w+)/(?P<action>subscribe|unsubscribe)/$', 'subscribe.views.event', name='event'),
    url(r'^units/', 'base.views.units', name='units'),
    url(r'^validate-chief/', 'subscribe.views.validate', name='validate'),

    url(r'^admin/', include(admin.site.urls)),
)
