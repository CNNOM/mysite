from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Vote
from .forms import VoteForm

def index(request):
    questions = Question.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {'questions': questions})

def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        form = VoteForm(request.POST, question=question)
        if form.is_valid():
            form.save()
            return redirect('results', question_id=question.id)
    else:
        form = VoteForm(question=question)
    
    return render(request, 'polls/question_detail.html', {
        'question': question,
        'form': form
    })

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})