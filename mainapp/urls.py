from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
    path('update-task/<str:pk>/', views.update_task, name="update-task"),
    path('delete-task/<str:pk>/', views.delete_task, name="delete-task"),
]
