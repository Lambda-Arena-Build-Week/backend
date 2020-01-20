import random
import math

class Room:
    def __init__(self, id, title, description, x=0, y=0):
        # creating a room_number for easier grid setup later, id is the coordinate in string
        self.id = id
        self.title = title
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __str__(self):
        return f"Room ID: {self.id}, Room Title: {self.title}, North: {self.n_to.id if self.n_to else False}, South: {self.s_to.id if self.s_to else False}, East: {self.e_to.id if self.e_to else False}, West: {self.w_to.id if self.w_to else False}"

    def __repr__(self):
        return str(self.id).zfill(6)

class World:
    def __init__(self, max=100):
        self.size = 0
        self.rooms = {}
        self.max = max
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
       
    def find_room(self, id):
        if id in self.rooms.keys():
            return self.rooms[id]
        else:
            return None

    def setup_world(self, room = None):
        if self.size == 0:
            new_room = Room(id = "0,0", title = "The Origin", description = "Initial Room set to coordinate [0, 0]")
            self.rooms[new_room.id] = new_room
            self.size += 1
            # print(new_room.id)
            self.setup_world(new_room)
        else:
            dirs = ["n", "e", "s", "w"]
            prob_1 = math.ceil(self.max / 50) 
            prob_08 = math.ceil(self.max / 25)
            prob = 1 if -(prob_1) <= room.x <= prob_1 and -(prob_1) <= room.y <= (prob_1) else (0.8 if -(prob_08) <= room.x <= prob_08 and -(prob_08) <= room.y <= prob_08 else 0.3)
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

        # if neighboring room at the direction exist, only make connection if rand is over 0.5
        if neighbor:
            if random.random() > 0.5:
                setattr(room, f"{dir}_to", neighbor)
                setattr(neighbor,f"{rev_dir[dir]}_to", room)

        # if not existing, create room and make connections    
        elif self.size < self.max:
            new_neighbor = Room(id = switcher.get(dir)[1], x = switcher.get(dir)[2], y = switcher.get(dir)[3], title = f"Testing Room [{switcher.get(dir)[1]}]", description = f"Additional Room at coord [{switcher.get(dir)[1]}]")
            self.rooms[new_neighbor.id] = new_neighbor
            self.size += 1

            self.x_max = new_neighbor.x if new_neighbor.x > self.x_max else self.x_max
            self.x_min = new_neighbor.x if new_neighbor.x < self.x_min else self.x_min
            self.y_max = new_neighbor.y if new_neighbor.y > self.y_max else self.y_max
            self.y_min = new_neighbor.y if new_neighbor.y < self.y_min else self.y_min
            
            setattr(room, f"{dir}_to", new_neighbor)
            setattr(new_neighbor, f"{rev_dir[dir]}_to", room)
            self.setup_world(new_neighbor)
        # return room

    # function unused with the new probability setup in setup_world function
    def check_max(self):
        print(self.size)

        origin_rm = self.find_room("0,0")
        rev_dir = {"n": "s", "s": "n", "e":"w", "w":"e"}

        switcher = {
            "n": [origin_rm.n_to, "0,1", 0, 1],
            "s": [origin_rm.s_to, "0,-1", 0, -1],
            "e": [origin_rm.e_to, "1,0", 1, 0],
            "w": [origin_rm.w_to, "-1,0", -1, 0]
        }
        for dir in switcher: 
            if self.size < self.max and switcher.get(dir)[0] is None:
                print("check_max is triggered")

                new_neighbor = Room(id = switcher.get(dir)[1], x = switcher.get(dir)[2], y = switcher.get(dir)[3], title = f"Testing Room [{switcher.get(dir)[1]}]", description = f"Additional Room at coord [{switcher.get(dir)[1]}]")
                
                self.rooms[new_neighbor.id] = new_neighbor
                self.size += 1

                setattr(origin_rm, f"{dir}_to", new_neighbor)
                setattr(new_neighbor, f"{rev_dir[dir]}_to", origin_rm)
                setup_world(new_neighbor)

    def print_world(self):
        x_offset = abs(self.x_min)
        y_offset = abs(self.y_min)
        width = x_offset + self.x_max + 1
        height = y_offset + self.y_max + 1
        print(f"Width: {width}, Height: {height}")
        # setting up grid for printing
        grid = [None] * height
        for i in range(len(grid)):
            grid[i] = [None] * width
            #print(grid[i])
       
        for i in self.rooms:
            grid[(self.rooms[i].y) + y_offset][(self.rooms[i].x) + x_offset] = self.rooms[i]
        
        print("***********")
        for i in reversed(range(len(grid))):
            str1 = ""
            str2 = ""
            str3 = ""
            for j in range(len(grid[i])):
                if grid[i][j]:
                    #check for north
                    if grid[i][j].n_to:
                        str1 += "     *    "
                    else:
                        str1 += "          "
                    #check for west
                    if grid[i][j].w_to:
                        str2 += "* "
                    else:
                        str2 += "  "
                    str2 += str(grid[i][j].id).zfill(6)
                    #check for east
                    if grid[i][j].e_to:
                        str2 += " *"
                    else:
                        str2 += "  "
                    #check for south
                    if grid[i][j].s_to:
                        str3 += "     *    "
                    else:
                        str3 += "          "
                else:
                    str1 += "          "
                    str2 += "          "
                    str3 += "          "
            print(str1)
            print(str2)
            print(str3)        
        print("***********")
        


new_world = World()
new_world.setup_world()
# check_max(new_world)
print("-----------------")
print(f"World Size: {new_world.size}")
print(f"Max X: {new_world.x_max}")
print(f"Min X: {new_world.x_min}")
print(f"Max Y: {new_world.y_max}")
print(f"Min Y: {new_world.y_min}")

new_world.print_world()
print("-----------------")

