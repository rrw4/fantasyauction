from django.conf.urls.defaults import patterns, include, url

from league import views

urlpatterns = patterns(
    'league.views',
    url(r'^{0}/rosters/$'.format(r'(?P<league_id>\d+)'), 'league_rosters', name='league_rosters'),
    url(r'^{0}/auctions/$'.format(r'(?P<league_id>\d+)'), 'league_auctions', name='league_auctions'),
    url(r'^{0}/$'.format(r'(?P<league_id>\d+)'), 'league_home', name='league_home'),
)

