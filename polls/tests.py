import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from .models import Choice, Question


class QuestionMethodTests(TestCase):
    def test_was_created_recently_with_future_question(self):
        """
        was_created_recently() должен возвращать False для вопросов с
        created в будущем.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(created=time)

        self.assertEqual(future_question.was_created_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_created_recently() должен возвращать False для вопросов с
        created в прошлом.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(created=time)
        self.assertEqual(old_question.was_created_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_created_recently() должен возвращать True для вопросов с
        created равным сегодняшней дате.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(created=time)
        self.assertEqual(recent_question.was_created_recently(), True)


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` published the given
    number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question.objects.create(question_text=question_text, created=time)

    return q


def create_choice(question_text, days):
    """
    Создает один вариант опроса
    :return: `Choice` object
    """
    q = create_question(question_text, days)
    c = Choice.objects.create(question=q, choice_text='asdsa')

    return c


class QuestionViewTest(TestCase):
    def test_index_view_with_no_questions(self):
        """
        Если вопросов нет, то должно выводиться соответствующее сообщение
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Вопросы с `created` в прошлом должны отображаться на главной странице.
        """
        create_choice(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Вопросы с `created` в будущем не должны отображаться на главной странице.
        """
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Даже если вопросы есть и в прошлом, и в будущем, должны отображаться
        только вопросы в прошлом
        """
        create_choice(question_text='Past question.', days=-30)
        create_choice(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        На главной странице может отображаться больше одного вопроса
        """
        create_choice(question_text='Past question 1.', days=-30)
        create_choice(question_text='Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

    def test_index_view_with_question_without_choice(self):
        """
        Вопросы без вариантов не должны отображаться
        """
        create_question(question_text='Past question 1.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], []
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        Должен возвращаться 404 для неопубликованных вопросов
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        """
        Должен возвращаться вопрос для опубликованных вопросов
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)


class QuestionIndexResultsTests(TestCase):
    def test_result_view_with_a_future_question(self):
        """
        Должен возвращаться 404 для неопубликованных вопросов
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_result_view_with_a_past_question(self):
        """
        Должен возвращаться вопрос для опубликованных вопросов
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)
