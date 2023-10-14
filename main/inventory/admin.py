from django.contrib import admin
from .models import Person, Device, Status
# Register your models here.

admin.site.register(Person)
admin.site.register(Device)
admin.site.register(Status)
