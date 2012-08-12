from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^poll/', include('poll.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'views.index'),
    url(r'^login/', login),
    url(r'^logout/', logout)
)