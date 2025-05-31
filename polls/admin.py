from django.contrib import admin
from .models import Question, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

class VoteAdmin(admin.ModelAdmin):
    list_display = ('choice', 'voter_name', 'vote_date')
    list_filter = ['vote_date', 'choice__question']
    search_fields = ['voter_name', 'choice__choice_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote, VoteAdmin)