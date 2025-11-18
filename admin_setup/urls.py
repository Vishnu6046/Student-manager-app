from django.urls import path
from . import views

urlpatterns = [
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/manage-students/', views.manage_students, name='manage_students'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('admin/manage-staff/', views.manage_staff, name='manage_staff'),
    path('delete_staff/<int:employee_id>/', views.delete_staff, name='delete_staff'),
    path('admin/manage-users/', views.manage_users, name='manage_users'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('admin_register_student/', views.admin_register_student, name='admin_register_student'),
    path('admin_register_staff/', views.admin_register_staff, name='admin_register_staff'),
    path('manage_department', views.manage_department, name='manage_department'),
    path('delete_department/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('manage_position', views.manage_position, name='manage_position'),
    path('delete_position/<int:pos_id>/', views.delete_position, name='delete_position'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('department-subject-overview/', views.department_subject_overview, name='dept_subject_overview'),
    path('subjects/add/<int:dept_id>/', views.add_subject, name='subject_add'),
]