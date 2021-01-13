from django.shortcuts import render, redirect
from django.contrib import messages
from Reservations.forms import FilteredListCars
from datetime import date

strr = []
endd = []


def home(request):
    from Reservations.models import Branch
    branches = Branch.objects.all()

    form = FilteredListCars()
    context = {'form': form}
    return render(request, 'reservations/home.html', context)


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
        branch = form.cleaned_data.get('branch')
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
def rent(request, id):
    from Reservations.models import Reservations
    from Reservations.models import Car
    take = strr[len(strr) - 1]
    give = endd[len(strr) - 1]
    car = Car.objects.get(id=id)
    car.takeDate.append(take)
    car.returnDate.append(give)
    car.save()
    Reservations.objects.create(receiveDate=take, deliveryDate=give, buyer=request.user.visitor, car=car)
    price = ((give - take).days) * car.price
    context = {'car': car, 'takedate': take, 'givedate': give, 'price': price}
    return render(request, 'reservations/rent.html', context)


def reservationsCar(request, id):
    from Reservations.models import Car
    car = Car.objects.get(id=id)
    context = {'car': car}
    return render(request, 'reservations/reservationsCar.html', context)


def aa(request):
    return render(request, 'reservations/filteredCarList.html', )
