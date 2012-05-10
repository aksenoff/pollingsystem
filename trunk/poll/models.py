from django.db import models
import datetime

class Poll(models.Model):
    caption = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='date published')
    def __unicode__(self):
        return self.caption
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description='Published today?'

class Question(models.Model):
    multiple_choice = models.BooleanField(verbose_name='allow multiple choice?')
    caption = models.CharField(max_length=500)
    number = models.SmallIntegerField()
    poll = models.ForeignKey(Poll)
    unique_together = ("poll", "number")
    is_optional = models.BooleanField()
    def __unicode__(self):
        return self.caption

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice = models.CharField(max_length=500)
    def __unicode__(self):
        return self.choice
    extra_field = models.BooleanField(verbose_name='has extra_field?')
    number = models.SmallIntegerField()
    unique_together = ("question", "number")

class Voting(models.Model):
    id = models.AutoField(primary_key=True)
    date_held = models.DateTimeField()
    poll = models.ForeignKey(Poll)
    closed = models.BooleanField(verbose_name='voting closed?')
    def __unicode__(self):
        return unicode(self.date_held) + u" " + unicode(self.poll)

class Ticket(models.Model):
    code = models.CharField(max_length=10, primary_key=True)#, editable=False)
    poll = models.ForeignKey(Poll)
    voting = models.ForeignKey(Voting, null=True, blank=True)
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=200, help_text="Extra info about the person", blank=True)
    def __unicode__(self):
        return self.code + u" " + unicode(self.poll)

class Result(models.Model):
    ticket = models.ForeignKey(Ticket)
    choice = models.ForeignKey(Choice)
    extra_field_text = models.CharField(max_length=1000, blank=True)
