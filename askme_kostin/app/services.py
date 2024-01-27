from django.core.paginator import Paginator
from .models import Question, Answer, questionLike, answerLike
from django.contrib import auth


def paginate(request, objects, per_page=10):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        if paginator.num_pages < int(page):
            page = paginator.num_pages
        elif 1 > int(page):
            page = 1
    except:
        page = 1
    return paginator.page(page)


def lastPage(objects, per_page=10):
    paginator = Paginator(objects, per_page)
    return paginator.num_pages


def questionLikes(request, questions):
    likes = []
    dislikes = []
    if request.user.is_authenticated:
        db_questions = list(questionLike.objects.filter(owner=request.user.profile))
        for like in db_questions:
            if like.question in questions:
                item = questionLike.objects.get(owner=request.user.profile, question=like.question)
                if item.value == 1:
                    likes.append(item.question)
                else:
                    dislikes.append(item.question)
    return likes, dislikes


def answersLikes(request, answers, question_id):
    likes = []
    dislikes = []
    if request.user.is_authenticated:
        if questionLike.objects.filter(owner=request.user.profile, question=question_id).exists():
            item = questionLike.objects.get(owner=request.user.profile, question=question_id)
            if item.value == 1:
                likes.append(item.question)
            elif item.value == -1:
                dislikes.append(item.question)
        db_answers = list(answerLike.objects.filter(owner=request.user.profile))
        for like in db_answers:
            if like.answer in answers:
                item = answerLike.objects.get(owner=request.user.profile, answer=like.answer)
                if item.value == 1:
                    likes.append(item.answer)
                elif item.value == -1:
                    dislikes.append(item.answer)

    return likes, dislikes


def answerSave(request, answer_form, question_id):
    answer = answer_form.save(user_id=request.user.id, question_id=question_id)
    if answer is None:
        answer_form.add_error(None, "Wrong answer form")
        return False
    else:
        return True


def questionSave(request, question_form):
    question = question_form.save(user_id=request.user.id)
    if question:
        return question
    else:
        question_form.add_error(None, "Please, enter data in all fields!")
        return None


def userSave(request, user_form):
    try:
        user = user_form.save()
        if user:
            auth.login(request, user)
            return True
        else:
            user_form.add_error(None, "Invalid data in fields")
            return False
    except:
        user_form.add_error(None, "This login is already used")
        user_form.add_error('username', "Wrong username")
        return False


def userLogin(request, login_form):
    user = auth.authenticate(request, **login_form.cleaned_data)
    if user:
        auth.login(request, user)
        return True
    else:
        login_form.add_error(None, "Sorry wrong login or password")
        login_form.add_error('password', "")
        login_form.add_error('username', "")
        return False


def userSettings(request, settings_form):
    user = settings_form.save()
    if user:
        return True
    else:
        settings_form.add_error(None, "Sorry wrong login or password")
        return False


def addQuestionRating(request, question, add_func):
    activation = add_func(user=request.user.profile, question=question)
    count = question.get_likes()
    return activation, count


def addAnswerRating(request, answer, add_func):
    activation = add_func(user=request.user.profile, answer=answer)
    count = answer.get_likes()
    return activation, count


def addCorrectMark(request, question, answer):
    if request.user.profile == question.author:
        Answer.objects.addCorrect(answer.id)
        return True
    else:
        return False
