from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sign_in/', views.sign_in_view, name='sign_in'),
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:id>/', views.student_delete, name='student_delete'),
]
