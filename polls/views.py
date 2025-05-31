from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Poll, Question, Vote, Choice
from .forms import VoteForm

def index(request):
    polls = Poll.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all().order_by('poll_questions__order')
    
    if request.method == 'POST':
        voter_name = request.POST.get('voter_name', '').strip() or None
        all_answered = True
        
        # Проверяем, что выбраны все ответы
        for question in questions:
            if not request.POST.get(f'question_{question.id}'):
                all_answered = False
                break
        
        if not all_answered:
            messages.error(request, "Пожалуйста, ответьте на все вопросы")
        else:
            # Сохраняем все ответы
            for question in questions:
                choice_id = request.POST.get(f'question_{question.id}')
                choice = Choice.objects.get(pk=choice_id)
                Vote.objects.create(
                    choice=choice,
                    voter_name=voter_name
                )
            return redirect('vote_success', poll_id=poll.id)
    
    # Подготавливаем формы для GET запроса
    forms = []
    for question in questions:
        form = VoteForm(question=question)
        forms.append((question, form))
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'forms': forms,
    })

def vote_success(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/vote_success.html', {'poll': poll})

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