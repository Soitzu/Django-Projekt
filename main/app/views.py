from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Report, Todo
from django.contrib import messages
from datetime import date, datetime
# Create your views here.

from .graph import get_graph


def home(request):
    # Get current Username and print it out to Welcome him
    current_user = request.user
    log_user = str(current_user)
    log_user = log_user.capitalize()
    # Welcome end

    # Get current hour, minutes and seconds
    time_now = datetime.now()
    hour = int(time_now.strftime("%H"))
    minute = int(time_now.strftime("%M"))
    second = int(time_now.strftime("%S"))
    # End

    if request.user.is_authenticated:
        my_todos = Todo.objects.all().values()
        if request.method == "POST":
            text = request.POST['description']
            create_todo = Todo(
                text=text, hour=hour, minute=minute, second=second, user=current_user
            )
            create_todo.save()
            messages.success(request, ("Todo saved successfully"))
            return redirect('home')

        return render(request, "home.html", {
            'log_user': log_user,
            'my_todos': my_todos,
            'hour': hour,

        })
    else:
        return redirect('login')


def redirect_view(request):
    return redirect("/home")


def report(request):
    if request.user.is_authenticated:
        current_user = request.user
        today = date.today()
        user = User.objects.get(username=current_user)
        if request.method == "POST":
            stnumber = request.POST["stnumber"]
            description = request.POST["description"]
            create_report = Report(
                stnumber=stnumber, text=description, user=current_user, date=today)
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


def delete_report(request, event_id):
    my_item = Report.objects.get(pk=event_id)
    my_item.delete()
    return redirect("my_reports")


def todos(request):
    return render(home)


def graph_view(request):
    graph = get_graph()

    return render(request, 'graph.html', {'graph': graph})
