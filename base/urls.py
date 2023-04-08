from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    # path(url, function, name='')
    path('',views.home,name='home'),
    path('room/',views.room),
    path('room/:id',views.room4),
]
