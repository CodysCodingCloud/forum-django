""" url and routes for chat funtions """

from django.urls import path

# from django.http import HttpResponse
from . import views

# routes
urlpatterns = [
    # path(url, function, name='variable to use in templates')
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("", views.home, name="home"),
    # path('room/',views.room),
    path("room/<str:pk>/", views.room_view, name="room"),
    path("create-room/", views.createRoom, name="create-room"),
    path("update-room/<str:pk>/", views.updateRoom, name="update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name="delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name="delete-message"),
    path("profile/<str:pk>/", views.user_profile, name="user"),
    path("update-user/", views.update_user, name="update_user"),
    path("topics/", views.topics_page, name="topics"),
    path("feed/<str:pk>/", views.activities_page, name="activity"),
    path("feed/", views.activities_page, name="activity"),
    # path('user/<str:pk>/', views.user, name='user'),
]
