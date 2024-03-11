from django.urls import path
from account import views

urlpatterns = [
    path('register', views.RegisterApiView.as_view()),
    path('login', views.LoginApiView.as_view()),
    path('user', views.UserApiView.as_view()),
    path('logout', views.LogoutApiView.as_view()),
]