
from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from phone_field import PhoneField


class Visitor(models.Model):
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    MANAGER = 'manager'
    ADMIN = 'admin'
    CUSTOMER = 'customer'

    ROLE_CHOICES = ((MANAGER, 'Manager'),
                    (ADMIN, 'Admin'),
                    (CUSTOMER, 'Customer'),
                    )
    role = models.CharField(choices=ROLE_CHOICES, blank=True, null=True, max_length=100)

    def __str__(self):
        return self.first_name


class Branch(models.Model):
    place = models.CharField(max_length=100)
    manager = models.ForeignKey(Visitor, models.SET_NULL, blank=True, null=True, )
    adress = models.CharField(max_length=300, null=True)
    phone = PhoneField(blank=True)
    mail = models.CharField(max_length=50, null=True)
    fax = PhoneField(blank=True)

    def __str__(self):
        return self.place


class Car(models.Model):
    GEAR_CATEGORY = (
        ('Automatic', 'Automatic'),
        ('Semi-Automatic', 'Semi-Automatic'),
        ('Manuel', 'Manuel'),
    )
    FUEL_CATEGORY = (
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
    )
    capacity = models.IntegerField()
    price = models.IntegerField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=150)
    gearType = models.CharField(max_length=100, verbose_name='Gear Type', choices=GEAR_CATEGORY)
    fuelType = models.CharField(max_length=100, verbose_name='Fuel Type', choices=FUEL_CATEGORY)
    isReserved = models.BooleanField(default=False, verbose_name='Reserved')
    isActive = models.BooleanField(default=True, verbose_name='Active')
    buyingDate = models.DateTimeField(auto_now_add=True, verbose_name='Purchase date')
    branch = models.ForeignKey(Branch, models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='media', blank=True, default='wp.png')
    takeDate = ArrayField(models.DateTimeField(), null=True, blank=True, default=list)
    returnDate = ArrayField(models.DateTimeField(), null=True, blank=True, default=list)

    def __str__(self):
        return self.brand + " " + self.model


class Reservations(models.Model):
    reservationDate = models.DateTimeField(auto_now_add=True, null=True, blank=True, )
    receiveDate = models.DateTimeField(verbose_name='Receive Date', null=True, blank=True)
    deliveryDate = models.DateTimeField(verbose_name='Delivery Date', null=True, blank=True)
    buyer = models.ForeignKey(Visitor, on_delete=models.CASCADE, verbose_name='Buyer', null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Car')

    def __str__(self):
        return self.buyer.first_name


class Message(models.Model):
    content = models.TextField(blank=True, null=True)
    reciever = models.ForeignKey(Visitor, models.SET_NULL, blank=True, null=True, )
