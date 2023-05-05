""" states and logic for your templates """
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.models import Room

from .serializars import RoomSerializer

# from base.api import serializers

# get_object_or_404, get_list_or_404


# pylint: disable=import-error
# GET POST PUT
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics',
        'GET /api/topics/:id',
    ]
    return Response(routes)
    # return JsonResponse(routes, safe=False)


@api_view(['GET'])
def getRooms(request):
    """to get JSON from Response http://127.0.0.1:8000/api/rooms?format=json"""
    print('accessed this????')
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return JsonResponse(serializer.data, safe=False)
    # return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    """to get JSON from Response http://127.0.0.1:8000/api/rooms?format=json"""
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    # return JsonResponse(serializer.data, safe=False)
    return Response(serializer.data)
