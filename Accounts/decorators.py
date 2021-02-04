from django.http import HttpResponse
from django.shortcuts import redirect


def admin_only(view_func):
    def wrapper_func(request, *arg, **kwargs):

        if request.user.visitor.role != 'admin':
            return redirect('home')

        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func


def manager_only(view_func):
    def wrapper_func(request, *arg, **kwargs):

        if request.user.visitor.role != 'manager':
            return redirect('home')

        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func


def manager_or_admin(view_func):
    def wrapper_func(request, *arg, **kwargs):

        if request.user.visitor.role != 'manager' and request.user.visitor.role != 'admin':
            return redirect('home')

        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func


def no_Admin(view_func):
    def wrapper_func(request, *arg, **kwargs):
        if request.user.visitor.role == 'admin':
            return redirect('manage')

        else:
            return view_func(request, *arg, **kwargs)

    return wrapper_func
