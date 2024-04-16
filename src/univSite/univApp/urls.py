from django.urls import path
from . import views

urlpatterns = [
    path("" , views.index, name="index"),
    path("admin/", views.admin, name="admin"),
    path("admin/F1/", views.F1, name="F1"),
    path('admin/F1/list_instructors/', views.list_instructors, name='list_instructors'),
    path("admin/F2/", views.F2, name="F2"),
    path('admin/F2/department_stats/', views.dept_stats, name='dept_stats'),
    path("admin/F3/", views.F3, name="F3"),
    path('admin/F3/prof_stats/', views.prof_stats, name='prof_stats'),
    path("professor/", views.professor, name="professor"),
    path("professor/list_sections/", views.sections, name="sections"),
    path("professor/F4/", views.F4, name="F4"),
    path("professor/F5/", views.F5, name="F5"),
    path("student/", views.student, name="student"),
    path("student/F6/", views.F6, name="F6")
]
