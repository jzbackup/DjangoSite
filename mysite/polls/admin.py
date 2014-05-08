from django.contrib import admin
from polls.models import Poll
from polls.models import Choice

# Register your models here.
class ChoiceInline(admin.StackedInline):
	model = Choice
	extra = 3
	
class PollAdmin(admin.ModelAdmin):
	fields = ['pub_date', 'question']
	
admin.site.register(Poll, PollAdmin)
#admin.site.register(Choice)

