from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import date, datetime
from app.models import Report, Todo
from .models import Status, Person, Device

# Create your views here.


def inventory_home(request):
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
        my_todos = Todo.objects.filter(user=request.user)
        if request.method == "POST":
            text = request.POST['description']
            if text == '':
                messages.success(
                    request, ("Nothing is not allowed! You have enough things to do ..."))
                return redirect('home')
            else:
                create_todo = Todo(
                    text=text, hour=hour, minute=minute, second=second, user=current_user
                )
                create_todo.save()
                messages.success(request, ("Todo saved successfully"))
                return redirect('home')

        return render(request, "inventory-home.html", {
            'log_user': log_user,
            'my_todos': my_todos,
            'hour': hour,

        })
    else:
        return redirect('login')


def create_status(request):

    if request.method == "POST":
        statusname = request.POST['statusname']
        status = Status(statusname=statusname)
        status.save()
        messages.success(request, ("Status successfully saved!"))

    return render(request, 'create_status.html', {})


def add_device(request):
    all_status = Status.objects.all().values()

    if request.method == "POST":
        model = request.POST['model']
        serialnumber = request.POST['serialnumber']
        statusname = request.POST['statusname']
        status_name = Status.objects.get(statusname=statusname)
        device = Device(model=model, serialnumber=serialnumber,
                        status=status_name)
        device.save()
        messages.success(request, ("Device added successfully!"))

    return render(request, 'add_device.html', {
        'all_status': all_status,
    })
