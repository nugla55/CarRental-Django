from django.urls import path

from Reservations import views

urlpatterns = [

    path('contact/', views.contactPage, name='contact'),
    path('about_us/', views.aboutUsPage, name='aboutUs'),
    path('filteredCarList/', views.filteredCarList, name='filteredCarList'),
    path('rent/<id>', views.rent, name='rent'),
    path('reservationscar/<id>', views.reservationsCar, name='reservationscar'),
    path('carlist/', views.carList, name='carlist'),
    path('carDetail<str:pk>/', views.carDetail, name='carDetail'),
    path('', views.home, name='home'),
    path('managerAddCar/<str:pk>', views.managerAddCar, name='managerAddCar'),
    path('managerRemoveCar/<str:pk>', views.managerRemoveCar, name='managerRemoveCar'),
    path('managermanagecar/<str:pk>', views.manager_manage_car, name='manager_manage_car'),
    path('payment/<str:pk>', views.payment, name='payment'),
    path('addManager/', views.addManager, name='addManager'),
    path('manage/', views.manage, name='manage'),
    path('managecar/<str:pk>', views.manage_car, name='manage_car'),
    path('addCar/', views.addCar, name='addCar'),
    path('removeCar/<str:pk>', views.removeCar, name='removeCar'),
    path('managebranch/<str:pk>', views.manage_branch, name='manage_branch'),
    path('addBranch/', views.addBranch, name='addBranch'),
    path('removeBranch/<str:pk>', views.removeBranch, name='removeBranch'),
    path('cancelBook/<str:pk>', views.cancelBook, name='cancelBook'),

]
