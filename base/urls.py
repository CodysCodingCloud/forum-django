from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    # path(url, function, name='variable to use in templates')
    path('',views.home, name='home'),
    # path('room/',views.room),
    path('room/<str:pk>/', views.room, name='room'),
]
