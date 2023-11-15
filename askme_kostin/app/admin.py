from django.contrib import admin
from .models import Question, Answer, Profile, Tag, questionLike, answerLike, profileLike

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(questionLike)
admin.site.register(answerLike)
admin.site.register(profileLike)
admin.site.register(Tag)
