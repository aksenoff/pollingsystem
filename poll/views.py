# Create your views here.
# encoding: utf8
from poll.models import Poll, Choice, Ticket
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
    
def vote(request, voting_id, ticket):
    voting = get_object_or_404(Voting, pk=poll_id)
    try:
        selected_choices = {}
        for question in p.question_set.all():
        	selected_choices[question.number] = int(request.POST['choice'+unicode(question.number)])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
       return render_to_response('poll/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
    	for question in selected_choices.keys():
    		pass # TODO: authorisation mechanism needed to implement db ticket insertion
#        # Always return an HttpResponseRedirect after successfully dealing
#        # with POST data. This prevents data from being posted twice if a
#        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))

def enter_ticket(request):
	return render_to_response('poll/enter_ticket.html', context_instance=RequestContext(request))

def poll_select(request):
	try:
		my_ticket = Ticket.objects.get(pk = int(request.POST['ticket']))
	except (KeyError, ValueError, Ticket.DoesNotExist):
		return render_to_response('poll/enter_ticket.html', {
			'error_message': "No such ticket",
			}, context_instance=RequestContext(request))
	else:
		return render_to_response('poll/select.html', {
			'ticket': my_ticket, 'votings': my_ticket.poll.voting_set.filter(closed=False)
			})