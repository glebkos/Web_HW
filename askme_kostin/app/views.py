from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .forms import LoginForm, RegisterForm, SettingsForm, QuestionForm, AnswerForm
from .models import Question, Answer, questionLike, answerLike
from .services import paginate, lastPage, questionLikes, answersLikes, answerSave, questionSave, userSave, userLogin,\
    userSettings, addQuestionRating, addAnswerRating, addCorrectMark


def index(request):
    questions = Question.objects.lastQuestions()
    likes, dislikes = questionLikes(request, questions)
    return render(request, 'index.html', {'title': 'New questions', 'page': paginate(request, questions),
                                          'likes': likes, 'dislikes': dislikes})


@csrf_protect
def question(request, question_id):
    answers = Answer.objects.lastAnswers()
    likes, dislikes = answersLikes(request, answers, question_id)

    if request.method == "GET":
        answer_form = AnswerForm()
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            if answerSave(request, answer_form, question_id):
                return redirect(request.path + '?page=' + str(lastPage(answers)))
    return_question = Question.objects.takeQuestion(question_id)
    answers = Answer.objects.takeAnswers(question_id)
    return render(request, 'question.html', context={'question': return_question, 'page': paginate(request, answers),
                                                     'form': answer_form, 'likes': likes, 'dislikes': dislikes})


@login_required(login_url='/login/', redirect_field_name='continue')
@csrf_protect
def add_question(request):
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = questionSave(request, question_form)
            if question:
                return redirect(reverse('question', args=[question.id]))
    return render(request, 'ask.html', context={'form': question_form})


def question_by_tag(request, question_tag):
    questions = Question.objects.tagSort(question_tag)
    likes, dislikes = questionLikes(request, questions)
    return render(request, 'index.html', {'title': f'Search by {question_tag}',
                                          'page': paginate(request, questions),
                                          'likes': likes, 'dislikes': dislikes})


def best_questions(request):
    best = Question.objects.hotQuestions()
    likes, dislikes = questionLikes(request, best)
    return render(request, 'index.html', {'title': f'Best searches', 'page': paginate(request, best),
                                          'likes': likes, 'dislikes': dislikes})


@csrf_protect
def register(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            if userSave(request, user_form):
                return redirect(request.GET.get('continue', '/'))
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
            if userLogin(request, login_form):
                return redirect(request.GET.get('continue', '/'))
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
            if userSettings(request, settings_form):
                return redirect(request.GET.get('continue', '/'))
    return render(request, 'settings.html', context={'form': settings_form})


@csrf_protect
@login_required
def like(request):
    id = request.POST.get('question_id')
    if id:
        question = get_object_or_404(Question, pk=id)
        activation, count = addQuestionRating(request, question, questionLike.objects.toggle_like)
    else:
        id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, pk=id)
        activation, count = addAnswerRating(request, answer, answerLike.objects.toggle_like)

    return JsonResponse({'count': count, 'activate': activation})


@csrf_protect
@login_required
def dislike(request):
    id = request.POST.get('question_id')
    if id:
        question = get_object_or_404(Question, pk=id)
        activation, count = addQuestionRating(request, question, questionLike.objects.distoggle_like)
    else:
        id = request.POST.get('answer_id')
        answer = get_object_or_404(Answer, pk=id)
        activation, count = addAnswerRating(request, answer, answerLike.objects.distoggle_like)

    return JsonResponse({'count': count, 'activate': activation})


@csrf_protect
@login_required
def correct(request):
    id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, pk=id)
    question_id = request.POST.get('question_id')
    question = get_object_or_404(Question, pk=question_id)
    success = addCorrectMark(request, question, answer)
    return JsonResponse({'success': success})


