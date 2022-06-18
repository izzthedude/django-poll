from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question, Choice

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    
    context = {
        'latest_questions': latest_questions,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)

def results(request, question_id):
    return HttpResponse(f"You're looking at the results of {question_id}.")

def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")