from django.shortcuts import render
from .models import Question, Answer
from .services import paginate


def index(request):
    questions = Question.objects.lastQuestions()
    return render(request, 'index.html', {'title': 'New questions', 'questions': paginate(request, questions)})


def question(request, question_id):
    return_question = Question.objects.takeQuestion(question_id)
    answers = Answer.objects.takeAnswers(question_id)
    return render(request, 'question.html', {'question': return_question, 'answers': paginate(request, answers)})


def add_question(request):
    return render(request, 'ask.html')


def question_by_tag(request, question_tag):
    questions = Question.objects.tagSort(question_tag)
    return render(request, 'index.html', {'title': f'Search by {question_tag}',
                                          'questions': paginate(request, questions)})


def best_questions(request):
    best = Question.objects.hotQuestions()
    return render(request, 'index.html', {'title': f'Best searches', 'questions': paginate(request, best)})


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')
