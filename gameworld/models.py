from django.db import models

# Create your models here.

class Room(models.Model):
    # rm_id used for identifying room based on a composition of coordinates
    rm_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=50, default="ROOM TITLE")
    description = models.CharField(max_length=500, default="ROOM DESCRIPTION")
    n_to = models.CharField(max_length=10, null=True, default=None) 
    s_to = models.CharField(max_length=10, null=True, default=None) 
    w_to = models.CharField(max_length=10, null=True, default=None) 
    e_to = models.CharField(max_length=10, null=True, default=None) 
    x = models.CharField(max_length=5, default=0)
    y = models.CharField(max_length=5, default=0)

    
