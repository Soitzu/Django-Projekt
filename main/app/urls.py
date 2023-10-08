from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.redirect_view),
    path('home/', views.home, name="home",),
    path('reports/', views.report, name="report"),
    path("show-reports/", views.all_reports, name="show_reports"),
    path("my-reports/", views.my_reports, name="my_reports")

]
