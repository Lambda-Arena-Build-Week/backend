from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
from util.world_generator import *
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
    
# new_world = World()
# new_world.setup_world()