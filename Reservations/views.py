from django.shortcuts import render, redirect
from django.contrib import messages
from Accounts.decorators import *
from Reservations.forms import *
from django.conf import settings
from django.core.mail import send_mail
from datetime import date
from django.contrib.auth.decorators import login_required, user_passes_test

strr = []
endd = []


@admin_only
def manage(request):
    from Reservations.models import Car, Branch

    branches = Branch.objects.all()
    cars = Car.objects.all()

    context = {'cars': cars, 'branches': branches}
    return render(request, 'reservations/home_admin.html', context)


@admin_only
def manage_car(request, pk):
    from Reservations.models import Car, Branch
    from Accounts.forms import CarForm

    car = Car.objects.get(id=pk)
    form = CarForm(instance=car)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('manage_branch', car.branch.id)

    context = {'car': car, 'form': form, }
    return render(request, 'reservations/manage_cars.html', context)


@admin_only
def manage_branch(request, pk):
    from Reservations.models import Car, Branch
    from Accounts.forms import ManageBranchForm

    branch = Branch.objects.get(id=pk)
    branches = Branch.objects.all()
    cars = Car.objects.filter(branch=branch)
    car = Car.objects.all()
    form = ManageBranchForm(instance=branch)
    if request.method == 'POST':
        form = ManageBranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('manage_branch', branch.id)

    context = {'branch': branch, 'branches': branches, 'cars': cars, 'car': car, 'form': form}
    return render(request, 'reservations/manage_branches.html', context)


def home(request):
    from Reservations.models import Branch
    branches = Branch.objects.all()

    form = FilteredListCars()
    context = {'form': form, 'branches': branches}
    return render(request, 'reservations/home.html', context)


@admin_only
def addCar(request):
    from Reservations.models import Car
    from Accounts.forms import AddCarForm
    form = AddCarForm()

    if request.method == "POST":
        form = AddCarForm(request.POST, request.FILES)
        if form.is_valid():
            messages.info(request, str(form.cleaned_data.get('brand')) + ' ' + str(
                form.cleaned_data.get('model')) + ' is successfully added')
            form.save()

            return (manage(request))

    context = {'form': form, }
    return render(request, 'forms/addCar.html', context)


@admin_only
def removeCar(request, pk):
    from Reservations.models import Car, Reservations

    car = Car.objects.get(id=pk)
    if car.isActive == True:
        reservation = Reservations.objects.filter(car=car)
        messages.info(request, str(car.brand) + ' ' + str(car.model) + ' is successfully removed')
        for i in reservation:
            subject = 'Reservation Cancelled!'
            message = 'Your Reservation has been cancelled \nGo back: 127.0.0.1:8000 ' \
                      '\nReservation Detail: ' \
                      '\nCar Branch: ' + str(car.branch) + '\nCar Brand and Model :' + str(car.brand) + ' ' \
                      + str(car.model) + '\nDate information : \n' + str(i.receiveDate) + '\n' + str(
                i.deliveryDate)
            from_email = settings.EMAIL_HOST_USER
            to_list = [i.buyer.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        car.delete()

    else:
        messages.info(request, str(car.brand) + ' ' + str(car.model) + ' is reserved now. You cannot delete!')

    return (manage(request))


@manager_only
def managerAddCar(request, pk):
    from Reservations.models import Branch
    from Accounts.forms import ManagerAddCarForm
    branch = Branch.objects.get(id=pk)
    form = ManagerAddCarForm()

    if request.method == "POST":
        form = ManagerAddCarForm(request.POST, request.FILES)
        if form.is_valid():
            messages.info(request, str(form.cleaned_data.get('brand')) + ' ' + str(
                form.cleaned_data.get('model')) + ' is successfully added')
            car = form.save()
            car.branch = branch
            car.save()
            return redirect('managerProfile')

    context = {'form': form}
    return render(request, 'forms/managerAddCar.html', context)



@manager_only
def managerRemoveCar(request, pk):
    from Reservations.models import Car, Reservations

    car = Car.objects.get(id=pk)
    if car.isActive == True:
        reservation = Reservations.objects.filter(car=car)
        messages.info(request, str(car.brand) + ' ' + str(car.model) + ' is successfully removed')
        for i in reservation:
            subject = 'Reservation Cancelled!'
            message = 'Your Reservation has been cancelled \nGo back: 127.0.0.1:8000 ' \
                      '\nReservation Detail: ' \
                      '\nCar Branch: ' + str(car.branch) + '\nCar Brand and Model :' + str(car.brand) + ' ' \
                      + str(car.model) + '\nDate information : \n' + str(i.receiveDate) + '\n' + str(
                i.deliveryDate)
            from_email = settings.EMAIL_HOST_USER
            to_list = [i.buyer.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        car.delete()
    else:
        messages.info(request, str(car.brand) + ' ' + str(car.model) + ' is reserved now. You cannot delete!')

    from Accounts.views import managerProfile

    return (managerProfile(request))


@manager_only
def manager_manage_car(request, pk):
    from Reservations.models import Car
    from Accounts.forms import CarForm

    car = Car.objects.get(id=pk)
    form = CarForm(instance=car)
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('managerProfile')

    context = {'car': car, 'form': form, }
    return render(request, 'reservations/manager_manage_cars.html', context)


@admin_only
def addManager(request):
    from Accounts.forms import SignupForm
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.info(request,
                          str(form.cleaned_data.get('first_name')) + ' ' + str(form.cleaned_data.get('last_name')) +
                          ' is successfully added')
            user = form.save()
            username = form.cleaned_data.get('username')
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            eml = form.cleaned_data.get('email')
            from Reservations.models import Visitor
            Visitor.objects.create(
                user=user,
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=eml,
                role='manager'
            )
            return redirect('manage')

    context = {'form': form}
    return render(request, 'forms/addManager.html', context)


@admin_only
def addBranch(request):
    from Reservations.models import Branch
    from Accounts.forms import AddBranchForm
    form = AddBranchForm

    if request.method == "POST":
        form = AddBranchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,
                          str(form.cleaned_data.get('place')) + ' is successfully added')
            return (manage(request))

    context = {'form': form, }
    return render(request, 'forms/addBranch.html', context)


@admin_only
def removeBranch(request, pk):
    from Reservations.models import Car, Branch, Reservations

    branch = Branch.objects.get(id=pk)
    car = Car.objects.filter(branch=branch)
    messages.info(request, str(branch.place) + ' is succesfully removed!')

    for i in car:
        reservation = Reservations.objects.filter(car=i)
        for j in reservation:
            subject = 'Reservation Cancelled!'
            message = 'Your Reservation has been cancelled \nGo back: 127.0.0.1:8000 ' \
                      '\nReservation Detail: ' \
                      '\nCar Branch: ' + str(i.branch) + '\nCar Brand and Model :' + str(i.brand) + ' ' \
                      + str(i.model) + '\nDate information : \n' + str(j.receiveDate) + '\n' + str(
                j.deliveryDate)
            from_email = settings.EMAIL_HOST_USER
            to_list = [j.buyer.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
    Car.objects.filter(branch=branch).delete()
    branch.delete()

    return (manage(request))


def carDetail(request, pk):
    from Reservations.models import Car
    cars = Car.objects.get(id=pk)
    context = {'cars': cars, }
    return render(request, 'reservations/carDetail.html', context)


def contactPage(request):
    from Reservations.models import Branch
    branches = Branch.objects.all()

    context = {'branches': branches}
    return render(request, 'reservations/contact.html', context)


def aboutUsPage(request):
    return render(request, 'reservations/aboutUs.html')


def carList(request, ):
    from Reservations.models import Car
    cars = Car.objects.all()
    context = {'cars': cars, }
    return render(request, 'reservations/carList.html', context)


def filteredCarList(request):
    from Reservations.models import Car
    from Reservations.models import Branch
    form = FilteredListCars(request.GET)
    if form.is_valid():
        str = form.cleaned_data.get('takeDate')
        strr.append(str)
        end = form.cleaned_data.get('returnDate')
        endd.append(end)
        branch = request.GET['branch']
    realBranch = Branch.objects.get(place=branch)
    cars = Car.objects.filter(branch=realBranch, isActive=True)
    filteredCars = []
    for car in cars:
        if not car.takeDate or (str > car.returnDate[len(car.takeDate) - 1]):
            filteredCars.append(car)
            continue
        for i in range(len(car.takeDate)):
            if (str < car.takeDate[i] and end < car.takeDate[i]) or (
                    str > car.returnDate[i] and end < car.takeDate[i + 1]):
                filteredCars.append(car)
    context = {'cars': filteredCars, 'takeDate': str, 'returnDate': end, }
    return render(request, 'reservations/filteredCarList.html', context)


from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def payment(request, pk):
    from Reservations.models import Reservations
    from Reservations.models import Car
    take = strr[len(strr) - 1]
    give = endd[len(strr) - 1]
    car = Car.objects.get(id=pk)
    price = ((give - take).days) * car.price

    form = PaymentForm()

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            Reservations.objects.create(receiveDate=take, deliveryDate=give, buyer=request.user.visitor, car=car)
            reservation = Reservations.objects.get(receiveDate=take, deliveryDate=give, buyer=request.user.visitor,
                                                   car=car)
            return redirect('rent', reservation.id)

    context = {'form': form, 'car': car, 'take': take, 'give': give, 'price': price}
    return render(request, 'forms/payment.html', context)


@login_required(login_url='login')
def rent(request, id):
    from Reservations.models import Reservations
    reservation = Reservations.objects.get(id=id)
    take = reservation.receiveDate
    give = reservation.deliveryDate
    car = reservation.car
    price = ((give - take).days) * car.price

    car.takeDate.append(take)
    car.returnDate.append(give)
    car.save()

    subject = 'Email sended!'
    message = 'Your Reservation has been accepted! \nGo back: 127.0.0.1:8000 ' \
              '\nReservation Detail: ' \
              '\nCar Branch: ' + str(car.branch) + '\nCar Brand and Model :' + str(car.brand) + ' ' \
              + str(car.model) + '\nDate information : \n' + str(reservation.receiveDate) + '\n' + str(
        reservation.deliveryDate)

    from_email = settings.EMAIL_HOST_USER
    to_list = [request.user.visitor.email, settings.EMAIL_HOST_USER]
    send_mail(subject, message, from_email, to_list, fail_silently=True)

    context = {'car': car, 'takedate': take, 'givedate': give, 'price': price}
    return render(request, 'reservations/rent.html', context)


def reservationsCar(request, id):
    from Reservations.models import Car
    car = Car.objects.get(id=id)
    context = {'car': car}
    return render(request, 'reservations/reservationsCar.html', context)


def aa(request):
    return render(request, 'reservations/filteredCarList.html', )


def cancelBook(request, pk):
    from Reservations.models import Reservations, Car
    reservation = Reservations.objects.get(id=pk)
    car = Car.objects.get(id=reservation.car.id)

    car.takeDate.remove(reservation.receiveDate)
    car.returnDate.remove(reservation.deliveryDate)
    car.save()

    Reservations.objects.get(id=pk).delete()

    user = request.user.visitor
    if user.role == 'customer':
        messages.info(request, 'Your reservation has been successfully canceled!')

        subject = 'Reservation Cancelled!'
        message = 'Your Reservation has been cancelled \nGo back: 127.0.0.1:8000 ' \
                  '\nReservation Detail: ' \
                  '\nCar Branch: ' + str(car.branch) + '\nCar Brand and Model :' + str(car.brand) + ' ' \
                  + str(car.model) + '\nDate information : \n' + str(reservation.receiveDate) + '\n' + str(
            reservation.deliveryDate)
        from_email = settings.EMAIL_HOST_USER
        to_list = [request.user.visitor.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('profile')
    else:
        messages.info(request, 'Reservation has been successfully canceled!')

        subject = 'Reservation Cancelled!'
        message = 'Your Reservation has been cancelled by the Manager! \nGo back: 127.0.0.1:8000 ' \
                  '\nReservation Detail: ' \
                  '\nCar Branch: ' + str(car.branch) + '\nCar Brand and Model :' + str(car.brand) + ' ' \
                  + str(car.model) + '\nDate information : \n' + str(reservation.receiveDate) + '\n' + str(
            reservation.deliveryDate)
        from_email = settings.EMAIL_HOST_USER
        to_list = [reservation.buyer.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('managerProfile')
