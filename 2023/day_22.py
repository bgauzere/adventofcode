from utils import read_content
import string 
import numpy as np
class Surface():
    def __init__(self, x1,y1,x2,y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2= y2

        self.points = set([(x,y) for x in range(x1,x2+1) for y in range(y1,y2+1)])

    def overlap(self, other):
        # Check if one rectangle is to the left of the other
        return self.points & other.points != set()
    def __str__(self):
        return f"({self.x1},{self.y1}) -> ({self.x2},{self.y2})"
    
class Space():
    def __init__(self):
        self.z_axis = {}
        self.bricks = []
        self.supports = {}
    
    def add_brick(self, brick):
        if brick.z not in self.z_axis:
            self.z_axis[brick.z] = [brick]
        else:
            self.z_axis[brick.z].append(brick)
        self.bricks.append(brick)

    def get_support(self, brick):
        if brick.id in self.supports:
            return self.supports[brick.id]
        else:
            return None
    def get_bricks(self):
        return self.bricks
    
    def find_bricks_in_surface(self, surface, z):
        bricks = []
        #print(f"searching for bricks in surface {surface.x1},{surface.y1},{surface.x2},{surface.y2} at level {z}")
        for delta in range(0, 6):
            for brick in self.z_axis.get(z-delta,[]):
                #print(brick)
                if brick.z + brick.height -1 >= z:
                    if brick.surface.overlap(surface):
                        bricks.append(brick)
        return bricks
    
    def max_level(self):
        return max(self.z_axis.keys())
    
    def print_level(self,level):
        bricks = self.z_axis.get(level,[])
        if len(bricks) == 0:
            return
        x_min = min([brick.x for brick in bricks])
        x_max = max([brick.x + brick.length -1 for brick in bricks])
        y_min = min([brick.y for brick in bricks])
        y_max = max([brick.y + brick.width -1 for brick in bricks])
        level_map = np.full((x_max+1,y_max+1),".")
        for brick in bricks:
            for p in brick.surface.points:
                if (level_map[p[0],p[1]] == "#"):
                    print(f"Alert {p} is already occupied")
                    breakpoint()
                level_map[p[0],p[1]] = "#"
        print(level_map)
    
class Brick3D():
    def __init__(self, x1, y1, z1, x2, y2, z2,id_brick):
        self.x = x1
        self.y = y1
        self.z = z1
        self.length = x2 -x1 +1
        self.width = y2 -y1 +1
        self.height = z2 -z1 +1
        self.id = id_brick

    @property
    def surface(self):
        return Surface(self.x,self.y,
                        self.x+self.length-1,self.y+self.width-1)

    def __str__(self):
        surface = self.surface
        return f"brick {self.id} is in surface {self.x},{self.y},{self.x+self.length-1 },{self.y+self.width -1} at level {self.z}"
    def __repr__(self):
        return f"{self.id} ({self.x},{self.y},{self.z}) -> ({self.x+self.length-1},{self.y+self.width-1},{self.z+self.height-1})"


def first(content):
    space = Space()
    id_brick = 0
    for l in content:
        p1,p2 = l.split("~")
        x1,y1,z1 = [int(c) for c in p1.split(",")]
        x2,y2,z2 = [int(c) for c in p2.split(",")]
        brick = Brick3D(x1,y1,z1,x2,y2,z2, id_brick)
        #print(f"brick {brick.id} at level {brick.z}")
        space.add_brick(brick)
        id_brick += 1
    #print(max([brick.height for brick in space.get_bricks()]))
    space.bricks.sort(key=lambda brick: brick.z)
    for level in range(1,space.max_level()+1):
        bricks_level = space.z_axis.get(level,[])
        if bricks_level:
            print(f"level {level} : {[brick.id for brick in bricks_level]}")
        to_move = []
        for brick in bricks_level:
            print(f"brick {brick.id} at level {brick.z}")
            brick_z = brick.z
            while(len(space.find_bricks_in_surface(brick.surface, brick_z-1 )) == 0):
                if brick_z == 1:
                    break
                brick_z -= 1
            if brick_z != brick.z:
                to_move.append((brick,brick_z))
        for brick, brick_z in to_move:
            space.z_axis[brick.z].remove(brick)
            print(f"{brick.id} from {brick.z} to {brick_z}")
            brick.z = brick_z
            if brick_z not in space.z_axis:
                space.z_axis[brick_z] = [brick]
            else:
                space.z_axis[brick_z].append(brick)
    #breakpoint()
    supports = {}
    is_supported_by = {}  
            
    for brick in space.get_bricks():
        surface = brick.surface
    #     #print(f"brick {brick.id}")
    #     z = brick.z
    #     z_below = z-1
    #     if z_below >= 1:
    #         bricks_below = space.find_bricks_in_surface(surface, z_below)
    #         if bricks_below:
    #             is_supported_by[brick] = bricks_below
    #             #print(f"brick {brick.id} is supported by {[brick_b.id for brick_b in bricks_below]}")
    #         # if (len(bricks_below) > 1):
    #         #     print(f"brick {brick} can be destroyed !")
         
        z_max = brick.z + brick.height
        #if z_below >= 1:   
        bricks_above = space.find_bricks_in_surface(surface, z_max)
        if bricks_above:
            supports[brick] = bricks_above
            #print(f"brick {brick.id} supports {[brick_b.id for brick_b in bricks_above]}")
            for brick_b in bricks_above:
                if brick_b not in is_supported_by:
                    is_supported_by[brick_b] = [brick]
                else:
                    is_supported_by[brick_b].append(brick)
    
    for brick in space.get_bricks():
        print(f"brick {brick.id}  at level {brick.z} is supported by {[brick_b.id for brick_b in is_supported_by.get(brick,[])]} and supports {[brick_b.id for brick_b in supports.get(brick,[])]}")
        if len(is_supported_by.get(brick, [])) == 0 and brick.z != 1:
            print(f"Alert brick {brick.id} at level {brick.z} !")
            #breakpoint()

    # for level in range(1,space.max_level()+1):
    #     #print(f"level {level} :")
    #     for brick in space.z_axis.get(level,[]):
    #         print(f"brick {brick.id} : {brick.surface}")
    #     space.print_level(level)

    nb_to_be_destroyed = 0
    
    def is_destroyable(brick,supports, is_supported_by):
        # une brick peut etre supprimée si no support
        support = supports.get(brick,None)
         
        if support is None or len(support) == 0:
            return True
        else: 
        # une brick peut etre supprimée chaque brick qu'elle support et supporte par > 1 brick
            for supported_brick in support: 
                if len(is_supported_by.get(supported_brick, [])) < 2:
                    return False
            return True

    nb_to_be_destroyed = 0
    for i,brick in enumerate(space.get_bricks()):
        if is_destroyable(brick,supports,is_supported_by):
            print(f"{i} : {brick.id} is going to be destroyed")
            nb_to_be_destroyed += 1  
        else:
            print(f"{brick.id} is not going to be destroyed")

    #breakpoint()
    return nb_to_be_destroyed


    

if __name__ == "__main__":
    content = read_content()
    #print(content)
    print(first(content))