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
    # print(topics)
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room_view(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    # for i in data:
    #   if i['id']==int(pk):
    #     room=i
    context = {'room': room, "room_messages": room_messages}
    return render(request, 'base/room.html', context)


# CRUD - Rooms
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('you are not the user')
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('/')
    return render(request, 'base/delete.html', {'obj': room})


def uer(request):
    return render(request, 'user.html')


def room4(request):
    return HttpResponse('room4')
