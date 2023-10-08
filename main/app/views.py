from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Report
from django.contrib import messages
import datetime
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html", {})
    else:
        return redirect('login')


def redirect_view(request):
    return redirect("/home")


def report(request):
    if request.user.is_authenticated:
        current_user = request.user
        user = User.objects.get(username=current_user)

        if request.method == "POST":
            stnumber = request.POST["stnumber"]
            description = request.POST["description"]
            create_report = Report(
                stnumber=stnumber, text=description, user=current_user)
            create_report.save()
            messages.success(request, ("Report saved successfully"))
        return render(request, "create_reports.html", {
            'user': user,
        })
    else:
        messages.success(request, ("Please Login first"))
        return redirect('login')


def all_reports(request):
    if request.user.is_authenticated:
        all_reports = Report.objects.all().values()

        return render(request, "all_reports.html", {
            'all_reports': all_reports,
        })
    else:
        messages.success(request, ("Please Login first"))
        return redirect('login')


def my_reports(request):
    if request.user.is_authenticated:
        my_reports = Report.objects.filter(user=request.user)

        return render(request, "my_reports.html", {
            'my_reports': my_reports,
        })
    else:
        messages.success(request, ("Please Login first"))
        return redirect('login')
