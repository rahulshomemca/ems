from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied


def admin_hr_required(view_func):
    def wrap(request, *args, **kwargs):
        allowed_roles = ["Admin", "HR"]
        if request.role in allowed_roles:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('polls_list'))
    return wrap


def admin_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == "Admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('polls_list'))
    return wrap


def emp_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == "Employee":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('polls_list'))
    return wrap

def hr_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.role == "HR":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('polls_list'))
    return wrap