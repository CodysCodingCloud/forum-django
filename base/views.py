from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# mockdata = [
#   {'id':1,'name':'adw'},
#   {'id':2,'name':'ert'},
#   {'id':3,'name':'jw5'},
# ]

# Create your views here.
def home(request):
  # queryset = ModelName.objects.all() | get() | filter() | exclude()
  # var      = Mn         att    method
  rooms = Room.objects.all()
  context = {'data':rooms}
  return render(request, 'base/home.html', context)


def room(request,pk):
  room = Room.objects.get(id=pk)
  # for i in data:
  #   if i['id']==int(pk):
  #     room=i
  context = {'room':room}
  return render(request, 'base/room.html', context)

def uer(request):
    return render(request, 'user.html')

def room4(request):
    return HttpResponse('room4')
