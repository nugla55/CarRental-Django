from .forms import SignupForm, VisitorForm, LoginForm
from Reservations.models import Visitor, Branch, Car, Reservations
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from Accounts.decorators import *
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.core.mail import send_mail
import pytz
from datetime import datetime, timedelta

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

        if username:
            if email:
                if password:
                    if (user is not None) and (Visitor.objects.filter(username=username, email=email).count() == 1):
                        login(request, user)
                        print(request.user.visitor.role)
                        if request.user.visitor.role == 'admin':
                            return redirect('manage')
                        else:
                            return redirect('home')
                    else:
                        messages.info(request, 'Username email or password is incorrect')
                else:
                    messages.info(request, 'Password should not be empty')
            else:
                messages.info(request, 'Email should not be empty')
        else:
            messages.info(request, 'Username should not be empty')


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
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=eml,
                role='customer'
            )
            subject = 'Email sended!'
            message = 'Welcome! \n' \
                      'go back: 127.0.0.1:8000 '
            from_email = settings.EMAIL_HOST_USER
            to_list = [eml, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

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

@manager_only
def managerProfile(request, ):
    visitor = request.user.visitor
    if request.method == 'POST':
        form = VisitorForm(request.POST, request.FILES, instance=visitor)
        if form.is_valid():
            form.save()
    branches = Branch.objects.filter(manager=visitor)
    now = datetime.now()- timedelta(hours=3)
    now = pytz.utc.localize(now)

    for i in branches:
        cars = Car.objects.filter(branch = i)
        print(i)
        for car in cars:
            reservations = Reservations.objects.filter(car=car)
            if len(reservations)>0:
                for reservation in reservations:
                    if (now>reservation.receiveDate) and (now<reservation.deliveryDate):
                        car.isActive = False
                        car.save()
                        break
                    else:
                        car.isActive = True
                        car.save()
            else:
                car.isActive = True
                car.save()

    form = VisitorForm(instance=visitor)
    context = {'branches': branches, 'form': form, }
    return render(request, 'registration/managerProfile.html', context)
