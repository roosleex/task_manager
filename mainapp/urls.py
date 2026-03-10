from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('login/', views.user_login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create-task/', views.create_task, name="create-task"),
    path('update-task/<str:pk>/', views.update_task, name="update-task"),
    path('delete-task/<str:pk>/', views.delete_task, name="delete-task"),
    path('all-tasks/', views.all_tasks, name="all-tasks"),
]
