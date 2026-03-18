from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('analytics/', views.analytics, name='analytics'),
]