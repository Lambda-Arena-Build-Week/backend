from django.db import models
from django.contrib.auth.models import User
from backend import settings
import uuid

class Room(models.Model):
    # rm_id used for identifying room based on a composition of coordinates
    rm_id = models.CharField(primary_key=True, max_length=10, unique=True, null=False)
    title = models.CharField(max_length=50, default="ROOM TITLE")
    description = models.CharField(max_length=500, default="ROOM DESCRIPTION")
    n_to = models.CharField(max_length=10, null=True) 
    s_to = models.CharField(max_length=10, null=True) 
    w_to = models.CharField(max_length=10, null=True) 
    e_to = models.CharField(max_length=10, null=True) 
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    player_ct = models.IntegerField(default=0)
    has_item = models.BooleanField(default = False)

    def make_connections(self, neighbor, dir):
           
        if dir == "n":
            self.n_to = neighbor.rm_id
            neighbor.s_to = self.rm_id
        elif dir == "s":
            self.s_to = neighbor.rm_id
            neighbor.n_to = self.rm_id
        elif dir == "e":
            self.e_to = neighbor.rm_id
            neighbor.w_to = self.rm_id
        elif dir == "w":
            self.w_to = neighbor.rm_id
            neighbor.e_to = self.rm_id
        else:
            return
        
        self.save()
        neighbor.save()
        
    def __str__(self):
        return f"Room: {self.rm_id}, N: {self.n_to}, S: {self.s_to}, W: {self.w_to}, E: {self.e_to}, Title: {self.title}, X: {self.x}, Y: {self.y}\n" 

    def add_player(self):
        self.player_ct += 1
        self.save()
    
    def remove_player(self):
        if self.player_ct > 0:
            self.player_ct -= 1
            self.save()

    def add_item(self):
        self.has_item = True
        self.save()


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default="A simple description of the item")
    category = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Item ID: {self.id}, Item Name: {self.item_name}, Item Description: {self.description}, Room: {self.room}"


# class Player(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
#     currentRoom = models.ForeignKey(Room, on_delete=models.CASCADE)
#     uuid = models.UUIDField(default = uuid.uuid4, unique=True)

#     def __str__(self):
#         return f"User: {self.user.id}, Current Room: {self.currentRoom.rm_id}, UUID: {self.uuid}"

#     def room_change(self, room):
#         self.currentRoom = room.rm_id
#         self.save()