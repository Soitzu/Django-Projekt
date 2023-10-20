from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('inventory/', views.inventory_home, name="inventory-home"),
    path('inventory/create_status', views.create_status, name='create_status'),
    path('inventory/add_device', views.add_device, name='add_device'),
    path('inventory/all_devices', views.all_devices, name='all_devices'),
    path('inventory/all_devices/<event_id>',
         views.delete_device, name='delete_device'),
    path('inventory/give_device/<device_id>',
         views.give_device, name='give_device'),
    path('inventory/remove_device/<event_id>',
         views.remove_device, name='remove_device'),


]
