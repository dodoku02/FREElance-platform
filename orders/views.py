from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResponseForm  # если ещё нет формы, создадим
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Message
from users.models import User

@login_required
def order_chat(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # доступ только участникам заказа
    if request.user != order.client and request.user != order.selected_freelancer:
        return redirect('dashboard')

    if request.method == 'POST':
        text = request.POST.get('text')

        if text:
            Message.objects.create(
                order=order,
                sender=request.user,
                text=text
            )

            return redirect('order_chat', order_id=order.id)

    messages = order.messages.all().order_by('created_at')

    return render(request, 'orders/chat.html', {
        'order': order,
        'messages': messages
    })
User = get_user_model()


@login_required
def select_freelancer(request, order_id, freelancer_id):
    order = get_object_or_404(Order, id=order_id)

    # защита
    if order.client != request.user:
        return redirect('dashboard')

    freelancer = get_object_or_404(User, id=freelancer_id)

    order.selected_freelancer = freelancer
    order.status = 'in_progress'
    order.save()

    messages.success(request, "Исполнитель выбран!")

    return redirect('order_responses', order_id=order.id)

@login_required
def respond_to_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    existing_response = Response.objects.filter(
        order=order,
        freelancer=request.user
    ).first()

    if existing_response:
        return redirect('order_detail', order_id=order.id)

    if request.method == 'POST':

        form = ResponseForm(request.POST)

        if form.is_valid():

            response = form.save(commit=False)
            response.order = order
            response.freelancer = request.user
            response.save()

            return redirect('order_list')

    else:
        form = ResponseForm()

    return render(request, 'orders/respond.html', {
        'form': form,
        'order': order
    })
@login_required
def my_orders(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    orders = Order.objects.filter(client=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    if request.user.role != 'freelancer':
        return redirect('dashboard')

    orders = Order.objects.filter(
        status='open',
        selected_freelancer__isnull=True
    ).order_by('-created_at')

    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

@login_required
def create_order(request):
    if request.user.role != 'client':
        return redirect('dashboard')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form})

@login_required
def order_responses(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # защита
    if order.client != request.user:
        return redirect('dashboard')

    responses = order.responses.all()

    return render(request, 'orders/order_responses.html', {
        'order': order,
        'responses': responses
    })