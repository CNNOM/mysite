from django.http import HttpResponse
from .models import Question

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_questions])
    return HttpResponse(output)