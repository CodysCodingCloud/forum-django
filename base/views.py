from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
# mockdata = [
#   {'id':1,'name':'adw'},
#   {'id':2,'name':'ert'},
#   {'id':3,'name':'jw5'},
# ]

# Create your views here.


def home(request):
    # queryset = ModelName.objects.all() | get() | filter() | exclude()
    # var      = Mn     q    att    method
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    # print(topics)
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    # for i in data:
    #   if i['id']==int(pk):
    #     room=i
    context = {'room': room, }
    return render(request, 'base/room.html', context)

# CRUD


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


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        print(request.POST)
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


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
