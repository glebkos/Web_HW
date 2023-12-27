from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from .models import Question, Answer, questionLike
from .services import paginate
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


def index(request):
    # print(request.user.profile)
    questions = Question.objects.lastQuestions()
    return render(request, 'index.html', {'title': 'New questions', 'page': paginate(request, questions)})


@csrf_protect
def question(request, question_id):
    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(user_id=request.user.id, question_id=question_id)
            if answer is None:
                answer_form.add_error(None, "Wrong answer form")
    return_question = Question.objects.takeQuestion(question_id)
    answers = Answer.objects.takeAnswers(question_id)
    return render(request, 'question.html', context={'question': return_question, 'page': paginate(request, answers),
                                                     'form': answer_form})


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def add_question(request):
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(user_id=request.user.id)
            if question is not None:
                return redirect(reverse('question', args=[question.id]))
            else:
                question_form.add_error(None, "Wrong question form")
    return render(request, 'ask.html', context={'form': question_form})


def question_by_tag(request, question_tag):
    questions = Question.objects.tagSort(question_tag)
    return render(request, 'index.html', {'title': f'Search by {question_tag}',
                                          'page': paginate(request, questions)})


def best_questions(request):
    best = Question.objects.hotQuestions()
    return render(request, 'index.html', {'title': f'Best searches', 'page': paginate(request, best)})


@csrf_protect
def register(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            try:
                user = user_form.save()
                if user is not None:
                    auth.login(request, user)
                    return redirect(request.GET.get('continue', '/'))
                else:
                    user_form.add_error(None, "Invalid data in fields")
            except:
                user_form.add_error(None, "This login is already used")
                user_form.add_error('username', "Wrong username")
        else:
            user_form.add_error(None, "Please, enter data in all fields ")
    return render(request, 'register.html', context={'form': user_form})


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
                login_form.add_error('password', "")
                login_form.add_error('username', "")
                print(login_form.errors)
    return render(request, 'login.html', context={'form': login_form})


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('continue', '/'))


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def settings(request):
    if request.method == "GET":
        settings_form = SettingsForm(None, initial=model_to_dict(request.user))
    if request.method == "POST":
        settings_form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if settings_form.is_valid():
            user = settings_form.save()
            if user is not None:
                return redirect(request.GET.get('continue', '/'))
            else:
                settings_form.add_error(None, "Sorry wrong login or password")
    return render(request, 'settings.html', context={'form': settings_form})


@csrf_protect
@login_required
def like(request):
    id = request.POST.get('question_id')
    question = get_object_or_404(Question, pk=id)
    questionLike.objects.toggle_like(user=request.user.profile, question=question)
    count = question.get_likes()
    print(count)

    return JsonResponse({'count': count})
