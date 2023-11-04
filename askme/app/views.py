from django.shortcuts import render


# Create your views here.

def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}'
        } for i in range(3)
    ]
    answers = [
        {
            'id': i,
            'title': f'Question {i}'
        } for i in range(2)
    ]
    return render(request, 'index.html', {'questions': questions})
    # return render(request, 'ask.html')
    # return render(request, 'question.html', {'answers': answers})
    # return render(request, 'login.html')
    # return render(request, 'register.html')
