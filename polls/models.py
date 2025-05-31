from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Returns True if the question was published within the last day."""
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.boolean = True  # Displays a checkmark in admin
    was_published_recently.short_description = "Опубликовано недавно?"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    choice_text = models.CharField(max_length=200, verbose_name="Вариант ответа")

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="Выбранный вариант")
    voter_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя голосующего")  # Allow blank
    vote_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")

    def __str__(self):
        return f"{self.voter_name or 'Anonymous'} voted for {self.choice.choice_text}"