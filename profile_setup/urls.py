from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_page, name='public'),
    path('login/student/', views.student_login, name='student_login'),
    path('login/staff/', views.staff_login, name='staff_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
]