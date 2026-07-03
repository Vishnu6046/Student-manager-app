from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.student_home, name='student_home'),
    path('staff/', views.staff_home, name='staff_home'),
    path('staff/edit/<int:student_id>/', views.edit_student, name='edit_student'),
    path('staff/mark/<int:mark_id>/edit/', views.edit_mark, name='edit_mark'),
    path('staff/add/', views.add_student, name='add_student'),
    path('add_mark/<int:student_id>/', views.add_mark, name='add_mark'),
    path('delete_mark/<int:mark_id>/', views.delete_mark, name='delete_mark'),
]