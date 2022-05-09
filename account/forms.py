from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    first_name = forms.CharField(label='Ваше имя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control'}
        )


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   label='Старый пароль')
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    label='Новый пароль')
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    label='Повторите новый пароль')
