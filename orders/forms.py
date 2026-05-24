from django import forms
from .models import Order
from .models import Response

class ResponseForm(forms.ModelForm):

    class Meta:
        model = Response

        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Расскажите, почему именно вы подходите для этого заказа'
            })
        }


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order

        fields = ['title', 'description', 'budget', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Создать дизайн сайта'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
                }),

            'budget': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 5000'
                }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Подробно опишите задачу',
                'rows': 5
            }),
        }