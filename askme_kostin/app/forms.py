from django import forms
from django.core.exceptions import ValidationError
from .models import Profile


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
        model = Profile
        fields = '__all__'
