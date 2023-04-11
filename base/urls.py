from django.urls import path
from django.http import HttpResponse
from . import views

# routes
urlpatterns = [
    # path(url, function, name='variable to use in templates')
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("register", views.registerView, name="register"),
    path("", views.home, name="home"),
    # path('room/',views.room),
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("user/<str:pk>/", views.home, name="user"),
    # path('user/<str:pk>/', views.user, name='user'),
]
