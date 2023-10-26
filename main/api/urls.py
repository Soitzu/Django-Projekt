from django.urls import path
from . import views

urlpatterns = [
    path('todo/', views.getTodo),
    path('add/', views.addTodo),
    path('delete/<int:pk>/', views.deleteTodo),

]
