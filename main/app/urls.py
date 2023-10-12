from django.contrib import admin
from django.urls import path, include
from . import views
from .views import graph_view

urlpatterns = [
    path("", views.redirect_view),
    path('home/', views.home, name="home",),
    path('home/<event_id>', views.delete_todo, name='delete_todo'),
    path('reports/', views.report, name="report"),
    path("show-reports/", views.all_reports, name="show_reports"),
    path("my-reports/", views.my_reports, name="my_reports"),
    path("my-reports/<event_id>", views.delete_report, name="delete_report"),
    path('graph/', graph_view, name='graph'),
    path('download_todo', views.download_todo, name='download_todo'),

]
