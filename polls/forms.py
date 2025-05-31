from django import forms
from .models import Choice

class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect,
        empty_label=None,
        required=True
    )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        if question:
            self.fields['choice'].queryset = question.choices.all()