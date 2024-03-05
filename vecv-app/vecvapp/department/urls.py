from django.urls import path
from department import views

# Create your views here.
urlpatterns = [
    path('addDepartment', views.DepartmentApiView.as_view()),
    path('getDepartment', views.DepartmentApiView.as_view()),
    path('deleteDepartment', views.DepartmentApiView.as_view()),
    path('updateDepartment', views.DepartmentApiView.as_view())
]