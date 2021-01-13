from django.urls import path

from .views import registerPage, managerProfile, profile, loginPage

urlpatterns = [

    path('login/', loginPage, name="login"),
    path('register/', registerPage, name='register'),
    path('profile/', profile, name='profile'),
    path('managerProfile/', managerProfile, name='managerProfile'),
]
