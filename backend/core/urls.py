from django.urls import path, re_path
from . import views

urlpatterns = [
    path('registration', views.CreateUser.as_view()),
    re_path(r'^api/v1/(($)|(?P<query>\w+)(=(?P<value>\d+)|($)?))', views.ApplicationInterface.as_view())
]