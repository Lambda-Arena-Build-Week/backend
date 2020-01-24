from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from rest_framework.decorators import api_view


@csrf_exempt
@api_view(["GET"])
def rooms(request):
    rooms = [{
        "rm_id": room.rm_id,
        "title": room.title,
        "description": room.description,
        "n_to": room.n_to,
        "s_to": room.s_to,
        "e_to": room.e_to,
        "w_to": room.w_to,
        "x": room.x,
        "y": room.y,
        "player_ct": room.player_ct,
        "has_item" : room.has_item,
        "items": [{"id" : item.id, "category" : item.category, "name" : item.item_name, "description" : item.description}
        for item in room.item_set.all()]
        }
        for room in Room.objects.all()]
    return JsonResponse(rooms, safe=False)
    
@api_view(["POST"])
def initialize(request):
    user = request.user
    room = Room.objects.get(rm_id = request.room)
    player = room.player_set.create(user = user)
    player.save()
    room.add_player()
    return JsonResponse({'id': player.id, 'uuid': player.uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': room.player_set.all()})
    

@api_view(["POST"])
def move(request):
    neighbors = {
        "n": f"{room.x},{room.y + 1}",
        "s": f"{room.x},{room.y - 1}",
        "e": f"{room.x + 1}, {room.y}",
        "w": f"{room.x - 1}, {room.y}"
    }
    user = request.user
    room = Room.objects.get(rm_id = request.room)
    direction = request.direction
    player = Player.objects.get(id = request.player)
    destination = Room.objects.get(rm_id = neighbors.get(direction))

    if destination:
        player.currentRoom = destination
        player.save()
        room.remove_player()
        destination.add_player()



