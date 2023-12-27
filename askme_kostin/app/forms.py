from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, Answer, Question, Tag
import datetime


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=4, widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data['password']
        if data == 'wrongpass':
            raise ValidationError('Wrong password!')
        return data


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    email = forms.EmailField(error_messages={"required": ""})
    first_name = forms.CharField(error_messages={"required": ""})
    last_name = forms.CharField(error_messages={"required": ""})

    password = forms.CharField(min_length=4, widget=forms.PasswordInput, error_messages={"required": ""})
    password_check = forms.CharField(min_length=4, widget=forms.PasswordInput, error_messages={"required": ""})

    # image = forms.ImageField()

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password != password_check:
            raise ValidationError("Passwords don't match")

    def save(self, commit=True):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(user=user, rating=0)
        return user


class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    # password = forms.CharField(min_length=4, widget=forms.PasswordInput)
    # password_check = forms.CharField(min_length=4, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    # def clean(self):
    #     password = self.cleaned_data['password']
    #     password_check = self.cleaned_data['password_check']
    #
    #     if password != password_check:
    #         raise ValidationError("Passwords don't match")

    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        recieved_avatar = self.cleaned_data.get('avatar')
        if recieved_avatar:
            profile.avatar = recieved_avatar
            profile.save()

        return user


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

    content = forms.CharField(max_length=2048, widget=forms.Textarea)
    tags = forms.CharField(max_length=256)

    def save(self, **kwargs):
        profile = Profile.objects.get(user_id=kwargs['user_id'])
        tags = []
        for item in self.cleaned_data['tags'].split():
            tag = Tag.objects.get(tag_name=item)
            if tag:
                tags.append(tag)
            else:
                tags.append(Tag.objects.create(tag_name=item))

        question = Question.objects.create(title=self.cleaned_data['title'], content=self.cleaned_data['content'],
                                           author=profile)
        question.tags.set(tags)
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']

    def save(self, user_id, question_id):
        profile = Profile.objects.get(user_id=user_id)
        question = Question.objects.get(id=question_id)
        return Answer.objects.create(content=self.cleaned_data['content'], author=profile, question=question)
