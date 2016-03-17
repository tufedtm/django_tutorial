from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('created')[:5]

    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    context = {
        'question': question
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    response = 'You\'re looking at the results of question %s.'
    return HttpResponse(response % question_id)


def vote(request, question_id):
    response = 'You\'re voting on question %s.'
    return HttpResponse(response % question_id)
