from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from datetime import date, datetime
from app.models import Report, Todo
from .models import Status, Person, Device, History
from django.conf import settings
import mimetypes
import os
from io import BytesIO
import base64

# qr codes
import segno

# Create your views here.


def inventory_home(request):
    # Get current Username and print Welcome
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
                return redirect('inventory-home')
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
        if request.method == "POST":
            drop_filter = request.POST['drop_filter']

            def filter_case(answer):
                filtered = request.POST['search']
                if answer == 'model':
                    return Device.objects.all().filter(
                        model__icontains=filtered).order_by('date')
                if answer == 'serialnumber':
                    return Device.objects.all().filter(
                        serialnumber__icontains=filtered).order_by('date')
                if answer == 'date':
                    return Device.objects.all().filter(
                        date__icontains=filtered).order_by('date')
                if answer == 'status':
                    return Device.objects.all().filter(
                        status__statusname__icontains=filtered).order_by('date')
                if answer == 'nothing':
                    messages.success(
                        request, ("Please choose a Filteroption!"))
                    return Device.objects.all().order_by('date')

            all_devices = filter_case(drop_filter)
            return render(request, 'all_devices.html', {
                'all_devices': all_devices,
            })
        else:
            print("blablaelse")
            all_devices = Device.objects.all().order_by('date')

            return render(request, 'all_devices.html', {
                'all_devices': all_devices,
            })
    else:
        return redirect('login')


def all_people(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            drop_filter = request.POST['drop_filter']

            def filter_case(answer):
                filtered = request.POST['search']
                if answer == 'fname':
                    return Person.objects.all().filter(
                        fname__icontains=filtered).order_by('stnumber')
                if answer == 'lname':
                    return Person.objects.all().filter(
                        lname__icontains=filtered).order_by('stnumber')
                if answer == 'stnumber':
                    return Person.objects.all().filter(
                        stnumber__icontains=filtered).order_by('stnumber')
                if answer == 'device':
                    return Person.objects.all().filter(
                        device__serialnumber__icontains=filtered).order_by('stnumber')
                if answer == 'nothing':
                    messages.success(
                        request, ("Please choose a Filteroption!"))
                    return Person.objects.all().order_by('stnumber')

            all_people = filter_case(drop_filter)
            return render(request, 'all_people.html', {
                'all_people': all_people,
            })
        else:
            print("blablaelse")
            all_people = Person.objects.all().order_by('stnumber')

            return render(request, 'all_people.html', {
                'all_people': all_people,
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


def order_people(request):
    if request.user.is_authenticated:
        all_people = Person.objects.all().order_by('stnumber')

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
        qrcode = segno.make(this_device.serialnumber)
        qr_bytes = BytesIO()
        # Du kannst hier 'png' durch andere unterstützte Formate ersetzen
        qrcode.save(qr_bytes, kind='png')

        # Konvertiere BytesIO in base64, um es im HTML-Bild-Tag anzuzeigen
        qr_base64 = base64.b64encode(qr_bytes.getvalue()).decode('utf-8')

        return render(request, 'info_device.html', {
            'this_device': this_device,
            'qr_base64': qr_base64,
        })

    else:
        return redirect('login')

def history_device(request, event_id):
    if request.user.is_authenticated:
        this_device = Device.objects.get(pk=event_id)
        this_history = History.objects.filter(device_id=event_id)

        return render(request, 'history_device.html', {
            'this_device': this_device,
            'this_history': this_history,
        })
    else:
        return redirect('login')

def test(request):
    return render(request, 'test.html', {})
