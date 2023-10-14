from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('inventory/', views.inventory_home, name="inventory-home"),
    path('inventory/create_status', views.create_status, name='create_status'),
    path('inventory/add_device', views.add_device, name='add_device'),


]
