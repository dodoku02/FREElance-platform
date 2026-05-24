from django.db import models
from django.conf import settings



class Order(models.Model):
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    STATUS_CHOICES = [
    ('open', 'Открыт'),
    ('in_progress', 'В работе'),
    ('completed', 'Завершён'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    selected_freelancer = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name='assigned_orders'
    )
    
class Response(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='responses')
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses_made')
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отклик от {self.freelancer} на {self.order}"  

class Message(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:20]}"
  

    