from django.shortcuts import render
from django.http import HttpResponse



data = [
  {'id':1,'name':'adw'},
  {'id':2,'name':'ert'},
  {'id':3,'name':'jw5'},
]

# Create your views here.
def home(request):
  context = {'data':data}
  return render(request, 'home.html', context)


def room(request):
  return render(request, 'room.html')

def uer(request):
    return render(request, 'user.html')

def room4(request):
    return HttpResponse('room4')
