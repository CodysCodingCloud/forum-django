""" url and routes for api """
from django.urls import path

# from django.http import HttpResponse
from . import views

# routes
urlpatterns = [
    # path(url, function, name='variable to use in templates')
    path("", views.getRoutes),
    path('rooms', views.getRooms),
    path('rooms/<str:pk>', views.getRoom),
]
