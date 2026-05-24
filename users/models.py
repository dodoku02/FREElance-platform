from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('freelancer', 'Фрилансер'),
        ('client', 'Заказчик'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        verbose_name='Роль'
    )
    bio = models.TextField("О себе", blank=True)
    skills = models.CharField("Навыки", max_length=255, blank=True)  # для фрилансера
    portfolio_link = models.URLField("Портфолио", blank=True)  # для фрилансера
    company_name = models.CharField("Название компании", max_length=255, blank=True)  # для заказчика