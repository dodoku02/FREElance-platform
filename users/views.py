from .forms import FreelancerOnboardingForm, ClientOnboardingForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserOnboardingForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from orders.models import Order
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def edit_profile(request):
    print("POST DATA:", request.POST)

    user = request.user

    if request.method == 'POST':

        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        user.bio = request.POST.get('bio', '')
        user.skills = request.POST.get('skills', '')
        user.portfolio_link = request.POST.get('portfolio_link', '')
        user.company_name = request.POST.get('company_name', '')

        user.save()
        

        return redirect('dashboard')

    return render(request, 'users/edit_profile.html', {
        'user': user
    })

@login_required
def dashboard(request):

    if request.user.role == 'client':

        orders = Order.objects.filter(client=request.user)

        return render(request, 'users/dashboard.html', {
            'orders': orders
        })

    else:

        open_orders = Order.objects.filter(
            status='open',
            selected_freelancer__isnull=True
            )
        my_orders = Order.objects.filter(selected_freelancer=request.user)

        return render(request, 'users/dashboard.html', {
            'open_orders': open_orders,
            'my_orders': my_orders
        })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('order_list')
        else:
            return render(request, 'users/login.html', {'error': 'Неверные данные'})

    return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически логиним
            return redirect('onboarding')  # сюда будем позже
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def onboarding(request):

    user = request.user

    if user.role == 'freelancer':
        form_class = FreelancerOnboardingForm
    else:
        form_class = ClientOnboardingForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = form_class(instance=user)

    return render(request, 'users/onboarding.html', {
        'form': form
    })

