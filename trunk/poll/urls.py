from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from poll.models import Poll, Voting

urlpatterns = patterns('',
    url(r'^$', 'poll.views.enter_ticket'),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Voting,
            template_name='poll/detail.html')),
    url(r'stats/$',
        ListView.as_view(
            model=Poll,
            template_name='poll/stats.html')),
    url(r'^stats/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll,
            template_name='poll/poll_stats.html'),
        name='poll_results'),
    url(r'^stats/(?P<pk>\d+)/tickets/$',
        DetailView.as_view(
            model=Poll,
            template_name='poll/poll_stats_tickets.html')),
    url(r'^stats/voting/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Voting,
            template_name='poll/voting_stats.html')),
    url(r'^stats/voting/(?P<pk>\d+)/tickets/$',
        DetailView.as_view(
            model=Voting,
            template_name='poll/voting_stats_tickets.html')),
    url(r'^(?P<voting_id>\d+)/vote/$', 'poll.views.vote'),
    url(r'^select/$', 'poll.views.poll_select'),
    url(r'^start/$', 
        ListView.as_view(
            model=Poll,
            template_name='poll/start_panel.html')),
    url(r'^start/(?P<poll_id>\d+)/$', 'poll.views.start_voting'),
    url(r'^stop/(?P<voting_id>\d+)/$', 'poll.views.stop_voting'),
)