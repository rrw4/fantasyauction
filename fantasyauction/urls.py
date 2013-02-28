from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

from fantasyauction import views

admin.autodiscover()

urlpatterns = patterns('fantasyauction.views',
    url(r'^$', 'home', name='home'),
    url(r'^leagues/', include('league.urls')),
    url(r'^auctions/', include('auction.urls')),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
    )
