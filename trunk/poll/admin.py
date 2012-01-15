from poll.models import Poll
from poll.models import Choice
from poll.models import Question
from poll.models import Voting
from poll.models import Ticket
from django.contrib import admin

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['caption']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [QuestionInline]
    list_display = ('caption', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
    search_fields = ['caption']
    date_hierarchy = 'pub_date'
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['caption']}),
        ('Options', {'fields': ['multiple_choice', 'number', 'is_optional']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('poll', 'number', 'caption', 'is_optional')
    list_filter = ['poll__caption']
    search_fields = ['caption']
    #date_hierarchy = 'pub_date'

admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Voting)
admin.site.register(Ticket)