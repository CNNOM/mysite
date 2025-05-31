from django.contrib import admin
from .models import Poll, Question, Choice, Vote, PollQuestion

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('question_text', 'created_at')
    search_fields = ['question_text']

class PollQuestionInline(admin.TabularInline):
    model = PollQuestion
    extra = 1

class PollAdmin(admin.ModelAdmin):
    inlines = [PollQuestionInline]
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['title']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)