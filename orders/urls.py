from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/chat/', views.order_chat, name='order_chat'),
    path('<int:order_id>/respond/', views.respond_to_order, name='respond'),  # добавили
    path('<int:order_id>/responses/', views.order_responses, name='order_responses'),  # для заказчика
    path('<int:order_id>/select/<int:freelancer_id>/', views.select_freelancer, name='select_freelancer'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('my/', views.my_orders, name='my_orders'),
    
]