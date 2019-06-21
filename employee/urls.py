from django.urls import path
from employee.views import *

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path('<id>/details/', employee_details, name='employee_details'),
    path('<id>/edit/', employee_edit, name='employee_edit'),
    path('add/', employee_add, name='employee_add'),
    path('<id>/delete/', employee_delete, name='employee_delete'),
]