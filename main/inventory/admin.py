from django.contrib import admin
from .models import Person, Device, Status, History
# Register your models here.

admin.site.register(Person)
admin.site.register(Device)
admin.site.register(Status)
admin.site.register(History)
