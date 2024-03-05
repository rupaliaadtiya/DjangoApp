from django.urls import path
from account import views

urlpatterns = [
    path('login', views.LoginApiView.as_view())
]