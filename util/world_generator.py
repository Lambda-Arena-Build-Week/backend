from gameworld.models import Room, Item, Player
import random
import math

Room.objects.all().delete()
Item.objects.all().delete()
Player.objects.all().delete()


class World:
    def __init__(self, max=100):
        self.size = 0
        self.rooms = {}
        self.max = max
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        self.inventory_max = math.ceil(self.max * .50)
        self.inventory_ct = 0
        self.inventory_size = 0
        
    def find_room(self, rm_id):
        if rm_id in self.rooms.keys():
            return self.rooms[rm_id]
        else:
            return None

    def setup_world(self, room = None):
        if self.size == 0:
            new_room = Room(rm_id = "0,0", title = "The Origin", description = "Initial Room set to coordinate [0, 0]")
            # SAVE NEW ROOM
            new_room.save()
            
            # adding to world room list
            self.rooms[new_room.rm_id] = new_room
            self.size += 1
            self.setup_world(new_room)
        else:
            dirs = ["n", "e", "s", "w"]
            prob_09 = math.ceil(self.max / 50) 
            prob_07 = math.ceil(self.max / 25)
            prob = 0.9 if -(prob_09) <= room.x <= prob_09 and -(prob_09) <= room.y <= (prob_09) else (0.7 if -(prob_07) <= room.x <= prob_07 and -(prob_07) <= room.y <= prob_07 else 0.3)
            # prob = 1 if -2 <= room.x <= 2 and -2 <= room.y <= 2 else (0.8 if -4 <= room.x <= 4 and -4 <= room.y <= 4 else 0.3)
            for dir in dirs:
                # making connection with either an existing room or create new room
                if random.random() < prob:
                    self.make_connection(room, dir)

    def make_connection(self, room, dir):
        switcher = {
            "n": [room.n_to, f"{room.x},{room.y + 1}", room.x, room.y + 1], 
            "s": [room.s_to, f"{room.x},{room.y - 1}", room.x, room.y - 1],
            "e": [room.e_to, f"{room.x + 1},{room.y}", room.x + 1, room.y],
            "w": [room.w_to, f"{room.x - 1},{room.y}", room.x - 1, room.y]
        }

        rev_dir = {"n": "s", "s": "n", "e":"w", "w":"e"}

        neighbor = self.find_room(switcher.get(dir)[1])

        # if neighboring room at the direction exist, only make connection if rand is <= 0.1
        if neighbor:
            if random.random() <= 0.1:
                room.make_connections(neighbor, dir)

        # if not existing, create room and make connections    
        elif self.size < self.max:
            new_neighbor = Room(rm_id = switcher.get(dir)[1], x = switcher.get(dir)[2], y = switcher.get(dir)[3], title = f"Room [{switcher.get(dir)[1]}]", description = f"Additional Room at coord [{switcher.get(dir)[1]}]")
            # SAVE NEW ROOM
            new_neighbor.save()

            # adding room to world room list
            self.rooms[new_neighbor.rm_id] = new_neighbor
            self.size += 1
            
            if self.size % (self.max / self.inventory_max) == 0:
                new_item = new_neighbor.item_set.create(item_name=f"Item {new_neighbor.rm_id}", description=f"Description for item {new_neighbor.rm_id}")
                self.inventory_size += 1
                new_neighbor.add_item()
                new_item.save()
            self.x_max = new_neighbor.x if new_neighbor.x > self.x_max else self.x_max
            self.x_min = new_neighbor.x if new_neighbor.x < self.x_min else self.x_min
            self.y_max = new_neighbor.y if new_neighbor.y > self.y_max else self.y_max
            self.y_min = new_neighbor.y if new_neighbor.y < self.y_min else self.y_min
            
            room.make_connections(new_neighbor, dir)

            self.setup_world(new_neighbor)