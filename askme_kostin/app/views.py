from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
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
    if request.method == "GET":
        login_form = RegisterForm()
    if request.method == "POST":
        login_form = RegisterForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Sorry wrong login or password")
                # login_form.errors['password'] = 'Wrong password'
    return render(request, 'register.html', context={'form': login_form, 'title': 'Register'})


@csrf_protect
def login(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Sorry wrong login or password")
                # login_form.errors['password'] = 'Wrong password'
    return render(request, 'login.html', context={'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('continue', '/'))


def settings(request):
    return render(request, 'settings.html', {'title': 'Settings'})
