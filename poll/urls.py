from django.urls import path
from poll.views import *

urlpatterns = [
    path('', index, name='polls_list'),
    path('all_poll', all_poll, name='all_poll'),
    path('<id>/details', details, name="poll_details"),
    path('<int:id>/', polls, name="single_details"),
    path('add/', PollView.as_view(), name='poll_add'),
    path('<int:id>/edit/', PollView.as_view(), name='poll_edit'),
    path('<int:id>/delete/', delete, name='poll_delete'),
]