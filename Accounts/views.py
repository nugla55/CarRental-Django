

from .forms import SignupForm, VisitorForm, LoginForm
from Reservations.models import Visitor,  Branch
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login

from django.contrib import messages


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if (user is not None) and (User.objects.filter(email=email).count() == 1):
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username email or password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)


def registerPage(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            eml = form.cleaned_data.get('email')
            Visitor.objects.create(
                user=user,
                username=user.username,
                first_name=firstname,
                last_name=lastname,
                email=eml,
                role='customer'
            )

            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def profile(request):
    visitor = request.user.visitor
    form = VisitorForm(instance=visitor)

    reservations = visitor.reservations_set.all()

    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES, instance=visitor)
        if form.is_valid():
            form.save()

    context = {'form': form, 'reservations': reservations, }
    return render(request, 'registration/profile.html', context)


def managerProfile(request, ):
    visitor = request.user.visitor
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES, instance=visitor)
        if form.is_valid():
            form.save()
    branches = Branch.objects.filter(manager=visitor)
    form = VisitorForm(instance=visitor)
    context = {'branches': branches, 'form': form, }
    return render(request, 'registration/managerProfile.html', context)
