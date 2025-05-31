from django import forms
from .models import Question, Choice, Vote

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['voter_name', 'choice']
        widgets = {
            'voter_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя (необязательно)',
                'class': 'form-control'
            }),
            'choice': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }
        required = {
            'voter_name': False,
        }

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['choice'].queryset = Choice.objects.filter(question=question)
            self.fields['choice'].label = ""  # Убираем label для вариантов ответа