from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Report(models.Model):
    stnumber = models.IntegerField()
    text = models.CharField(max_length=500)
    date = models.DateField(null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "ST: " + str(self.stnumber) + " | " + "Erstellt von: " + str(self.user)


class Todo(models.Model):
    # Get the current Time
    hour = models.IntegerField(null=True)
    minute = models.IntegerField(null=True)
    second = models.IntegerField(null=True)
    # End
    date = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=500)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
