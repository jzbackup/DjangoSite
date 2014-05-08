from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('books.views',
	url(r'^$', 'index'),
	url(R'^time/$', 'current_datetime'),
	#url(r'^search_form/$', 'search_form'),
	url(r'^search/$', 'search')
)