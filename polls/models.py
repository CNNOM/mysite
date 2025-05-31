from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="Текст вопроса")
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        default=timezone.now,  # Используем default вместо auto_now_add для гибкости
        editable=False
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        verbose_name="Вопрос",
        related_name='choices'
    )
    choice_text = models.CharField(max_length=200, verbose_name="Вариант ответа")

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.choice_text

class Poll(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название опроса")
    description = models.TextField(blank=True, verbose_name="Описание")
    questions = models.ManyToManyField(
        Question, 
        through='PollQuestion', 
        verbose_name="Вопросы",
        related_name='polls'
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

class PollQuestion(models.Model):
    poll = models.ForeignKey(
        Poll, 
        on_delete=models.CASCADE,
        related_name='poll_questions'
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE,
        related_name='poll_questions'
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок вопроса")
    
    class Meta:
        ordering = ['order']
        unique_together = [['poll', 'question']]
        verbose_name = "Вопрос в опросе"
        verbose_name_plural = "Вопросы в опросах"

    def __str__(self):
        return f"{self.poll.title} - {self.question.question_text} (порядок: {self.order})"

class Vote(models.Model):
    choice = models.ForeignKey(
        Choice, 
        on_delete=models.CASCADE, 
        verbose_name="Выбранный вариант",
        related_name='votes'
    )
    voter_name = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Имя голосующего"
    )
    vote_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")

    class Meta:
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"

    def __str__(self):
        return f"{self.voter_name or 'Аноним'} проголосовал за {self.choice.choice_text}"