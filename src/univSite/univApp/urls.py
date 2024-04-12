from django.urls import path
from . import views

urlpatterns = [
    path("" , views.index, name="index"),
    path("admin/", views.admin, name="admin"),
    path("admin/F1/", views.F1, name="F1"),
    path("admin/F2/", views.F2, name="F2"),
    path("admin/F3/", views.F3, name="F3"),
    path("professor/", views.professor, name="professor"),
    path("student/", views.student, name="student"),
]
