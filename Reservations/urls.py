from django.urls import path

from Reservations import views

urlpatterns = [

    path('contact/', views.contactPage, name='contact'),
    path('about_us/', views.aboutUsPage, name='aboutUs'),
    path('filteredCarList/', views.filteredCarList, name='filteredCarList'),
    path('rent/<id>', views.rent, name='rent'),
    path('reservationscar/<id>', views.reservationsCar, name='reservationscar'),
    path('carlist/', views.carList, name='carlist'),
    path('', views.home, name='home'),

]
