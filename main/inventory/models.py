from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Status(models.Model):
    statusname = models.CharField(max_length=50)

    def __str__(self):
        return self.statusname


class Device(models.Model):
    model = models.CharField(max_length=50)
    serialnumber = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + " | " + str(self.model) + " | " + str(self.status)


class Person(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    stnumber = models.IntegerField()
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "ST: " + str(self.stnumber) + " | " + str(self.lname) + ", " + str(self.fname)
