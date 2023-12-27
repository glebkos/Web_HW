from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


class TagManager(models.Manager):
    pass


class QuestionManager(models.Manager):
    def tagSort(self, tag):
        return self.filter(tags__tag_name=tag)

    def lastQuestions(self):
        return self.order_by("-creation_date")

    def takeQuestion(self, id):
        try:
            return self.get(id=id)
        except ObjectDoesNotExist:
            raise Http404("Poll does not exist")

    def hotQuestions(self):
        return self.order_by("-rating")


class QuestionLikeManager(models.Manager):
    def toggle_like(self, user, question):
        if not self.filter(owner=user, question=question).exists():
            self.create(owner=user, question=question, value=1)
            question.rating += 1
            question.save()
        else:
            self.filter(owner=user, question=question).delete()
            question.rating -= 1
            question.save()


class AnswersManager(models.Manager):
    def takeAnswers(self, question_id):
        return self.filter(question__id=question_id)


class Profile(models.Model):
    avatar = models.ImageField(blank=True, null=True, default='default.png', upload_to='avatar/%Y/%m/%d')
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField('self', through='profileLike', through_fields=('profile', 'owner'))


class Tag(models.Model):
    tag_name = models.CharField(max_length=256, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.tag_name


class Question(models.Model):
    title = models.CharField(max_length=256)
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(Profile, max_length=256, on_delete=models.SET_NULL, null=True, related_name='questionAuthor')
    creation_date = models.DateTimeField(null=False, default=timezone.now)
    tags = models.ManyToManyField(Tag)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(Profile, through='questionLike', through_fields=('question', 'owner'))

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_likes(self):
        return self.rating


class Answer(models.Model):
    content = models.CharField(max_length=2048)
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='answerAuthor')
    creation_date = models.DateTimeField(null=False, default=timezone.now)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, unique=False)
    rating = models.IntegerField(default=0)
    likes = models.ManyToManyField(Profile, through='answerLike', through_fields=('answer', 'owner'))

    objects = AnswersManager()

    def __str__(self):
        return self.content


class questionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField()

    objects = QuestionLikeManager()


class answerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField()


class profileLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profileOwner')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    value = models.BooleanField()

