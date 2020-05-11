# encoding: utf8
from poll.models import Poll, Choice, Ticket, Voting, Result
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
# from django.template import RequestContext
from django.urls import reverse
import datetime, random
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.core import serializers
    
def vote(request, voting_id):
    voting = get_object_or_404(Voting, pk=voting_id)
    try:
        selected_choices = {}
        for question in voting.poll.question_set.all():
            selected_choices[question] = int(request.POST['choice'+str(question.number)])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
       return render('poll/detail.html', {
            'voting': voting,
            'error_message': u"Вы неправильно проголосовали",
        })
    else:
        current_ticket = Ticket.objects.get(pk=int(request.session['ticket']))
        for question in selected_choices.keys():
            Result.objects.create(ticket=current_ticket, choice=Choice.objects.get(question=question, number=selected_choices[question]))
            current_ticket.voting = voting
            current_ticket.voted = True
            current_ticket.save()
            # request.session["ticket"] = current_ticket
#        # Always return an HttpResponseRedirect after successfully dealing
#        # with POST data. This prevents data from being posted twice if a
#        # user hits the Back button.
        return HttpResponseRedirect(reverse('index'))

def clear_ticket(request):
    if "ticket" in request.session:
        del request.session["ticket"]
    return HttpResponseRedirect(reverse('poll_select'))

def poll_select(request):
    if "ticket" in request.session:
        current_ticket = Ticket.objects.get(pk=int(request.session['ticket']))
        return render(request, 'poll/select.html', {
                'ticket': current_ticket, 'votings': current_ticket.poll.voting_set.filter(closed=False)
                })
    else:
        if "ticket" in request.POST:
            try:
                passed_ticket = Ticket.objects.get(pk=int(request.POST['ticket']))
            except (KeyError, ValueError, Ticket.DoesNotExist):
                return render(request, 'poll/enter_ticket.html', {
                    'error_message': "Вы ввели недействительный тикет",
                    })
            else:
                request.session["ticket"] = request.POST['ticket']
                return HttpResponseRedirect(reverse('poll_select'))
        else:
            return render(request, 'poll/enter_ticket.html')

@login_required(login_url="/login/")
def start_voting(request, poll_id):
    current_poll = Poll.objects.get(pk=poll_id)
    current_voting = Voting.objects.create(date_held = datetime.datetime.now(), poll=current_poll, closed=False)
    return render(request, 'poll/voting_in_progress.html', {
        'voting': current_voting,
        })

@login_required(login_url="/login/")
def stop_voting(request, voting_id):
    current_voting = Voting.objects.get(pk=voting_id)
    current_voting.closed = True;
    current_voting.save()
    return render(request, 'poll/voting_stopped.html', {
        'voting': current_voting,
        })

@login_required(login_url="/login/")
def poll_list(request):
    return ListView.as_view(
                model=Poll,
                template_name='poll/start_panel.html')(request)

@login_required(login_url="/login/")
def stats(request):
    return ListView.as_view(
                model=Poll,
                template_name='poll/stats.html')(request)

@login_required(login_url="/login/")
def poll_stats(request, poll_id):
    return DetailView.as_view(
                model=Poll,
                template_name='poll/poll_stats.html')(request, pk=poll_id)

@login_required(login_url="/login/")
def poll_stats_tickets(request, poll_id):
    return DetailView.as_view(
                model=Poll,
                template_name='poll/poll_stats_tickets.html')(request, pk=poll_id)

@login_required(login_url="/login/")
def voting_stats(request, voting_id):
    voting = Voting.objects.get(pk=voting_id)
    results = []
    for question in voting.poll.question_set.all():
        for choice in question.choice_set.all():
            result = choice.result_set.filter(ticket__voting__id=voting_id).count()
            results.append((question.number, choice.number, result))
    return render(request, 'poll/voting_stats.html', {
        'results': results,
        'voting': voting,
        })

@login_required(login_url="/login/")
def voting_stats_tickets(request, voting_id):
    voting = Voting.objects.get(pk=voting_id)
    results = []
    for question in voting.poll.question_set.all():
        for choice in question.choice_set.all():
            result = choice.result_set.filter(ticket__voting__id=voting_id).count()
            voters = Ticket.objects.filter(voting__id=voting_id)
            voters2 = []
            for voter in voters:
                for x in choice.result_set.filter(ticket__voting__id=voting_id):
                    for r in voter.result_set.all(): # fuck my brain!
                        if r.id==x.id:
                            voters2.append(voter.name)
            results.append((question.number, choice.number, result, voters2))
    return render(request, 'poll/voting_stats_tickets.html', {
        'results': results,
        'voting': voting,
        })

def display_voting(request, voting_id):
    if "ticket" in request.session and Voting.objects.get(pk=voting_id) in Ticket.objects.get(pk=int(request.session['ticket'])).poll.voting_set.all():
        return DetailView.as_view(
                    model=Voting,
                    template_name='poll/detail.html')(request, pk=voting_id)
    else:
        return HttpResponseRedirect(reverse('views.index'))

@login_required(login_url='/login/')
def votings_in_progress_list(request):
    return render(request, 'poll/votings_in_progress_list.html', {
                'votings': Voting.objects.filter(closed=False)
                })

@login_required(login_url='/login/')
def generate_tickets(request):
    if request.method != 'POST':
        return render(request, 'poll/ticket_generation_settings.html', {
            'polls': Poll.objects.all()
            })
    else:
        if 'form1' in request.POST:
            try:
                request.session["poll_id"] = int(request.POST['poll'])
                poll = Poll.objects.get(pk=int(request.POST['poll']))
                request.session["num_tickets"] = int(request.POST['num_tickets'])
                request.session["num_spare_tickets"] = int(request.POST['num_spare_tickets'])
            except:
                return render(request, 'poll/ticket_generation_settings.html', {
                    'error_message': u'Заполните настройки правильно',
                    'polls': Poll.objects.all(),
                    })
            else:
                return render(request, 'poll/ticket_generation_settings2.html', {
                    'tickets': range(request.session["num_tickets"]),
                    'num_spare_tickets': request.session["num_spare_tickets"],
                    })
        elif 'form2' in request.POST:
            try:
                request.session["names"] = []
                request.session["tickets"] = []
                for i in range(request.session["num_tickets"]):
                    request.session["names"].append(request.POST["name"+str(i)])
            except:
                return render(request, 'poll/ticket_generation_settings2.html', {
                    'error_message': u'Заполните настройки правильно',
                    'tickets': range(request.session["num_tickets"]),
                    'num_spare_tickets': request.session["num_spare_tickets"],
                    })
            else:
                poll = Poll.objects.get(pk=request.session["poll_id"])
                for i in range(request.session["num_tickets"]):
                    # generate unique code for each ticket
                    code = random.randint(100000000000000, 999999999999999)
                    Ticket.objects.create(code=code, poll=poll, name=request.session["names"][i])
                    request.session["tickets"].append((code, request.session["names"][i]))
                for i in range(request.session["num_spare_tickets"]):
                    code = random.randint(100000000000000, 999999999999999)
                    name = "spare_ticket"+str(i+1)
                    Ticket.objects.create(code=code, poll=poll, name=name)
                    request.session["tickets"].append((code, name))                
                return render(request, 'poll/tickets_for_print.html', {
                    'tickets': request.session["tickets"],
                    'poll': poll,
                    })


