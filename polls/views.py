from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Question, Vote
from .forms import VoteForm

def index(request):
    polls = Poll.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all().order_by('poll_questions__order')
    
    # Создаем список форм для каждого вопроса
    forms = []
    for question in questions:
        form = VoteForm(question=question)
        forms.append((question, form))
    
    # Обработка POST запросов
    if request.method == 'POST':
        # Находим вопрос по ID из скрытого поля
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        form = VoteForm(request.POST, question=question)
        
        if form.is_valid():
            vote = form.save(commit=False)
            vote.save()
            return redirect('poll_results', poll_id=poll.id)
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'forms': forms  # Передаем список кортежей (вопрос, форма)
    })


def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.choice = form.cleaned_data['choice']
            vote.save()
            return redirect('poll_results', poll_id=question.poll.id)
    else:
        form = VoteForm()
        form.fields['choice'].queryset = question.choice_set.all()
    
    return render(request, 'polls/question_detail.html', {
        'question': question,
        'form': form
    })

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/poll_results.html', {'poll': poll})