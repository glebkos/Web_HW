from django.shortcuts import render


# Create your views here.

def index(request):
    questions = [
        {
            'id': i,
            'title': f'Question {i}'
        } for i in range(3)
    ]
    return render(request, 'ask.html', {'questions': questions})
