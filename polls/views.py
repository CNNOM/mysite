from django.shortcuts import render, redirect, get_object_or_404
from .models import Poll, Question, Vote
from .forms import VoteForm

def index(request):
    polls = Poll.objects.all().order_by('-pub_date')
    return render(request, 'polls/index.html', {'polls': polls})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = poll.questions.all().order_by('poll_questions__order')
    
    forms = []
    for question in questions:
        form = VoteForm(question=question)
        forms.append((question, form))
    
    if request.method == 'POST':
        voter_name = request.POST.get('voter_name', '').strip() or None
        
        # Проверяем, что на все вопросы есть ответы
        all_answered = True
        votes_to_create = []
        
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}', None)
            if not choice_id:
                all_answered = False
                break
                
            choice = Choice.objects.get(pk=choice_id)
            votes_to_create.append(Vote(
                choice=choice,
                voter_name=voter_name
            ))
        
        if all_answered and votes_to_create:
            Vote.objects.bulk_create(votes_to_create)
            return redirect('poll_results', poll_id=poll.id)
    
    return render(request, 'polls/poll_detail.html', {
        'poll': poll,
        'forms': forms
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