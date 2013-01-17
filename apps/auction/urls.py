from django.conf.urls.defaults import patterns, include, url

from auction import views

urlpatterns = patterns(
    'auction.views',
    url(r'^{0}/$'.format(r'(?P<auction_id>\d+)'), 'auction_home', name='auction_home'),
)

