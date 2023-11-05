"""
URL configuration for askme project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.best_questions, name='best_questions'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.add_question, name='ask'),
    path('tag/<question_tag>/', views.question_by_tag, name='tag_search'),
    path('signup/', views.login, name='signup'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls)
]
