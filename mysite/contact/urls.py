from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('contact.views',
	url(r'^$', 'contact'),
	url(R'^thanks/$', 'thanks'),
)