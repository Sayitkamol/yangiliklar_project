from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='parol',
                               widget=forms.PasswordInput)
    password_2 = forms.CharField(label='parolni takrorlang',
                                 widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Parollaringiz mos kelmadi!")
        return data['password_2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']