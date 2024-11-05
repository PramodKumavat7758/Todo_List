from asyncio import create_task
from tkinter.font import names

from django.urls import path
from django.views.generic import DeleteView
from django.contrib.auth.views import LogoutView
from . import  views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, DeleteTask, UserLogin, UserRegister

urlpatterns =[

    # Show list of tasks
    path('',TaskList.as_view(), name='tasks'),

    #Details for task
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),

    # CRUD operations on tasks
    path('create_task/', TaskCreate.as_view(), name='create-task'),
    path('update_task/<int:pk>/', TaskUpdate.as_view(), name='update-task'),
    path('delete_task/<int:pk>', DeleteTask.as_view(), name='delete-task'),

    #User Login and logout
    path('login/', UserLogin.as_view(), name="login"),

    path('logout/',LogoutView.as_view(next_page='login'), name="logout"),

    # Register new user
    path('register/',UserRegister.as_view(), name="register"),


]