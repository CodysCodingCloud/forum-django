""" states and logic for your templates """
from django.shortcuts import render, redirect

# get_object_or_404, get_list_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

# pylint: disable=import-error
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm
from .models import Room, Topic, Message


def login_view(request):
    """login user"""
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as err:
            print(err)
            messages.error(request, err)
            messages.error(request, 'User does not exist')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            messages.error(request, 'Username or Password do not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def register_view(request):
    """registers user using post"""
    page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'an error occurred during registration')
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def logout_view(request):
    """logs out user"""
    logout(request)
    return redirect('/')


def home(request):
    """root dir"""
    # queryset = ModelName.objects.all() | get() | filter() | exclude()
    # var      = Mn     q    att    method
    queryset = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=queryset)
        | Q(name__icontains=queryset)
        | Q(description__icontains=queryset)
    ).order_by('-updated')
    topics = Topic.objects.all()
    room_count = rooms.count()
    recent_messages = Message.objects.all()
    # print(topics)
    context = {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'recent_messages': recent_messages,
    }
    return render(request, 'base/home.html', context)


def room_view(request, pk):
    """retrieves many to one relationships - messages to room"""
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    # orders by -descending vs ascending
    participants = room.participants.all().order_by('username')
    print(participants)
    if request.method == "POST":
        message = Message.objects.create(
            body=request.POST.get('body'), user=request.user, room=room
        )
        room.participants.add(request.user)
        # message.save()
        # room.message_set(request.POST)
        return redirect('room', pk=room.id)
    if request.method == "DELETE":
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        "room_messages": room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)


# CRUD - Rooms
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            # name=request.POST.get('name')
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # initial form data
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not the user')
    if request.method == 'POST':
        # needs initial data to know what to update
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    # forms can only use GET | POST requests (idempotent)
    # forms cannot sent DELETE or PUT requests because they are not idempotent
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('not the owner')
    if request.method == 'POST':
        message.delete()
        return redirect('/room/' + str(message.room.id))
    return render(request, 'base/delete.html', {'obj': message})


def userprofile(request, pk):
    userinfo = User.objects.get(id=pk)
    rooms = user.room_set.all().order_by('-created')
    context = {'user': userinfo, 'rooms': rooms}
    return render(request, 'base/profile.html', context)


def room4(request):
    return HttpResponse('room4')
