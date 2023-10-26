from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import date, datetime
from app.models import Report, Todo
from .models import Status, Person, Device, User
import mimetypes
import os

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

    if request.user.is_authenticated:
        if request.method == "POST":
            statusname = request.POST['statusname']
            status = Status(statusname=statusname)
            status.save()
            messages.success(request, ("Status successfully saved!"))

        return render(request, 'create_status.html', {})
    else:
        return redirect('login')


def create_device(request):
    if request.user.is_authenticated:
        all_status = Status.objects.all().values()

        if request.method == "POST":
            model = request.POST['model']
            serialnumber = request.POST['serialnumber']
            statusname = request.POST['statusname']
            if statusname == 'nothing':
                messages.success(request, ("Please select a Status!"))
                return redirect('add_device')

            if serialnumber == '' or model == '':
                messages.success(request, ('Blank spaces arent allowed!'))
                return redirect('add_device')

            status_name = Status.objects.get(statusname=statusname)
            device = Device(model=model, serialnumber=serialnumber,
                            status=status_name)
            device.save()
            messages.success(request, ("Device added successfully!"))

        return render(request, 'create_device.html', {
            'all_status': all_status,
        })
    else:
        return redirect('login')


def all_devices(request):
    if request.user.is_authenticated:
        all_devices = Device.objects.all()

        return render(request, 'all_devices.html', {
            'all_devices': all_devices,
        })
    else:
        return redirect('login')


def delete_device(request, event_id):
    if request.user.is_authenticated:
        current_device = Device.objects.filter(pk=event_id)
        current_device.delete()

        return redirect('all_devices')
    return redirect('login')


def give_device(request, device_id):
    if request.user.is_authenticated:
        current_device = Device.objects.get(pk=device_id)
        all_person = Person.objects.all()

        if request.method == 'POST':
            person = request.POST['person']
            current_person = Person.objects.filter(
                id=person).update(device=current_device)
            new_status = Status.objects.get(statusname="Vergeben")
            current_device.status = new_status
            current_device.save()

            # Just for the message
            show_person = Person.objects.get(id=person).fname
            # End
            messages.success(
                request, ("Added Devive to " + show_person))
            return redirect('all_devices')

        return render(request, 'give_device.html', {
            'current_device': current_device,
            'all_person': all_person,
        })
    return redirect('login')


def remove_device(request, event_id):
    if request.user.is_authenticated:
        current_device = Device.objects.get(pk=event_id)
        current_owner = Person.objects.get(device=current_device)

        if request.method == "POST":
            new_status = Status.objects.get(statusname="Verfügbar")
            current_device.status = new_status
            current_device.save()
            current_owner = Person.objects.filter(
                device=current_device).update(device='')
            return redirect('all_devices')

        return render(request, 'remove_device.html', {
            'current_device': current_device,
            'current_owner': current_owner,
        })
    else:
        return redirect('login')


def all_people(request):
    if request.user.is_authenticated:
        all_people = Person.objects.all()

        return render(request, 'all_people.html', {
            'all_people': all_people,
        })
    else:
        return redirect('login')


def delete_people(request, event_id):
    if request.user.is_authenticated:
        current_person = Person.objects.get(pk=event_id)
        current_person.delete()
        messages.success(request, ("Person successfully deleted!"))

        return redirect('all_people')

    else:
        return redirect('login')


def create_people(request):
    if request.user.is_authenticated:
        status = Status.objects.get(statusname="Verfügbar")
        all_devices = Device.objects.filter(status=status)
        print(status)
        print(all_devices)

        if request.method == "POST":
            fname = request.POST['fname']
            lname = request.POST['lname']
            stnumber = request.POST['stnumber']
            device = request.POST['device']
            this_device = Device.objects.get(model=device)

            new_person = Person(fname=fname, lname=lname,
                                stnumber=stnumber, device=this_device)
            new_person.save()
            new_status = Status.objects.get(statusname='Vergeben')
            this_device.status = new_status
            this_device.save()

            messages.success(request, ("Person successfully created!"))
            return redirect('create_people')
        return render(request, 'create_people.html', {
            'all_devices': all_devices,
        })
    else:
        return redirect('login')


def info_device(request, event_id):
    if request.user.is_authenticated:
        this_device = Device.objects.get(pk=event_id)
        return render(request, 'info_device.html', {
            'this_device': this_device,
        })
    else:
        return redirect('login')


def test(request):
    return render(request, 'test.html', {})
