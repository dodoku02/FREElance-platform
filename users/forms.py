from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class FreelancerOnboardingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['skills', 'portfolio_link', 'bio']


class ClientOnboardingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['company_name', 'bio']
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Выберите роль")

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

class UserOnboardingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'skills', 'portfolio_link', 'company_name']