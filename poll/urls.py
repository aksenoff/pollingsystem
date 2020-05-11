from django.urls import re_path
from django.views.generic import DetailView
from poll.models import Poll, Voting
from poll.views import poll_select, display_voting, stats, poll_stats, poll_stats_tickets, voting_stats, voting_stats_tickets, vote, clear_ticket, poll_list, votings_in_progress_list, start_voting, stop_voting, generate_tickets 

urlpatterns = [
    re_path(r'^$', poll_select, name='poll_select'),
    re_path(r'^(?P<voting_id>\d+)/$', display_voting),
    re_path(r'stats/$', stats),
    re_path(r'^stats/(?P<poll_id>\d+)/$', poll_stats),
    re_path(r'^stats/(?P<poll_id>\d+)/tickets/$', poll_stats_tickets),
    re_path(r'^stats/voting/(?P<voting_id>\d+)/$', voting_stats),
    re_path(r'^stats/voting/(?P<voting_id>\d+)/tickets/$',voting_stats_tickets),
    re_path(r'^(?P<voting_id>\d+)/vote/$', vote),
    re_path(r'^clear_ticket/$', clear_ticket),
    re_path(r'^start/$', poll_list),
    re_path(r'^stop/$', votings_in_progress_list),
    re_path(r'^start/(?P<poll_id>\d+)/$', start_voting),
    re_path(r'^stop/(?P<voting_id>\d+)/$', stop_voting),
    re_path(r'^generate/', generate_tickets),
]