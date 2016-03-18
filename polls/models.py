import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField('Текст вопроса', max_length=200)
    created = models.DateTimeField('Дата создания')

    def __str__(self):
        return self.question_text

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now
    was_created_recently.admin_order_field = 'created'
    was_created_recently.boolean = True
    was_created_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос')
    choice_text = models.CharField('Текст ответа', max_length=200)
    votes = models.IntegerField('Количество голосов', default=0)

    def __str__(self):
        return self.choice_text
