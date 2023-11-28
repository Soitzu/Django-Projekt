from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('inventory/', views.inventory_home, name="inventory-home"),
    path('inventory/create_status', views.create_status, name='create_status'),
    path('inventory/create_device', views.create_device, name='create_device'),
    path('inventory/all_devices', views.all_devices, name='all_devices'),
    path('inventory/all_devices/<event_id>',
         views.delete_device, name='delete_device'),
    path('inventory/give_device/<device_id>',
         views.give_device, name='give_device'),
    path('inventory/remove_device/<event_id>',
         views.remove_device, name='remove_device'),
    path('inventory/all_people', views.all_people, name='all_people'),
    path('inventory/all_people/<event_id>',
         views.delete_people, name='delete_people'),
    path('inventory/create_people', views.create_people, name='create_people'),
    path('inventory/info_device/<event_id>',
         views.info_device, name='info_device'),
    path('inventory/test', views.test, name='test'),
    path('inventory/order_people', views.order_people, name='order-people'),
    path('inventory/history/<event_id>', views.history_device, name='history_device'),



]
