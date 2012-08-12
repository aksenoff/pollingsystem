from django.conf.urls.defaults import *
from django.views.generic import DetailView
from poll.models import Poll, Voting

urlpatterns = patterns('',
    url(r'^$', 'poll.views.poll_select'),
    url(r'^(?P<voting_id>\d+)/$', 'poll.views.display_voting'),
    url(r'stats/$', 'poll.views.stats'),
    url(r'^stats/(?P<poll_id>\d+)/$', 'poll.views.poll_stats'),
    url(r'^stats/(?P<poll_id>\d+)/tickets/$', 'poll.views.poll_stats_tickets'),
    url(r'^stats/voting/(?P<voting_id>\d+)/$', 'poll.views.voting_stats'),
    url(r'^stats/voting/(?P<voting_id>\d+)/tickets/$','poll.views.voting_stats_tickets'),
    url(r'^(?P<voting_id>\d+)/vote/$', 'poll.views.vote'),
    url(r'^clear_ticket/$', 'poll.views.clear_ticket'),
    url(r'^start/$', 'poll.views.poll_list'),
    url(r'^stop/$', 'poll.views.votings_in_progress_list'),
    url(r'^start/(?P<poll_id>\d+)/$', 'poll.views.start_voting'),
    url(r'^stop/(?P<voting_id>\d+)/$', 'poll.views.stop_voting'),
    url(r'^generate/', 'poll.views.generate_tickets'),
)