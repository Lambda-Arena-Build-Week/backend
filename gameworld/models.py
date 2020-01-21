from django.db import models


class Room(models.Model):
    # rm_id used for identifying room based on a composition of coordinates
    rm_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=50, default="ROOM TITLE")
    description = models.CharField(max_length=500, default="ROOM DESCRIPTION")
    n_to = models.CharField(max_length=10, null=True) 
    s_to = models.CharField(max_length=10, null=True) 
    w_to = models.CharField(max_length=10, null=True) 
    e_to = models.CharField(max_length=10, null=True) 
    x = models.CharField(max_length=5, default=0)
    y = models.CharField(max_length=5, default=0)

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
        
    def __str__(self):
        return f"Room: {self.rm_id}, N: {self.n_to}, S: {self.s_to}, W: {self.w_to}, E: {self.e_to}, Title: {self.title}, X: {self.x}, Y: {self.y}\n" 


    
