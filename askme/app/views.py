from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'AWESOME question {i}',
        'tag': ['blabla'],
        'score': i
    } for i in range(100)
]

ANSWERS = [
    {
        'id': i,
        'content': f'Question {i}'
    } for i in range(20)
]


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


def index(request):
    return render(request, 'index.html', {'title': 'New questions', 'questions': paginate(request, QUESTIONS)})


def question(request, question_id):
    return render(request, 'question.html', {'question': QUESTIONS[question_id], 'answers': paginate(request, ANSWERS)})


def add_question(request):
    return render(request, 'ask.html')


def question_by_tag(request, question_tag):
    answer = []
    for i in range(0, len(QUESTIONS)):
        if question_tag in QUESTIONS[i]['tag']:
            answer.append(QUESTIONS[i])
    return render(request, 'index.html', {'title': f'Search by {question_tag}', 'questions': paginate(request, answer)})


def best_questions(request):
    best = sorted(QUESTIONS, key=lambda x: x['score'], reverse=True)
    return render(request, 'index.html', {'title': f'Best searches', 'questions': paginate(request, best)})


def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')
