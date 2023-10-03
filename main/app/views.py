from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime

# Create your views here.


def home(request):
    return render(request, "home.html", {})


def redirect_view(request):
    return redirect("/home")
