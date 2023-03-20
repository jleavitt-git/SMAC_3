import numpy as np
from enum import Enum
from enum import IntEnum

gridSize = 10

class type(Enum):
    NONE     = -1
    SCAFFOLD = 0
    STRAIGHT = 1
    ANGLE    = 2

class orientation(IntEnum):
    NONE = -1
    ANY = 0
    X   = 1
    Y   = 2
    Z   = 3
    XN   = 4
    YN   = 5
    ZN   = 6

class rotation(Enum):
    NONE = -1
    ANY = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4

class Block:
    def __init__(self, id, xs, ys, zs, critical = None, depth = 0, type=type.NONE, orientation=orientation.NONE, rotation=orientation.NONE, strongLink=None, prioritized=False, pathToGround=[]):
        self.id = id
        self.xs = xs
        self.ys = ys
        self.zs = zs
        self.critical = critical
        self.depth = depth
        self.type = type
        self.orientation = orientation
        self.rotation = rotation
        self.strongLink=strongLink
        self.prioritized=prioritized
        self.pathToGround=pathToGround
        
    def toString(self):
        print("ID: ", self.id, " X: ", self.xs, " Y: ", self.ys, " Z: ", self.zs)
    def asArray(self):
        return [self.xs,self.ys,self.zs]
    
def validateBlocks(blocks, n):
    gridSize = n
    #First validate each block coordinates individually
    for b in blocks:
        if(b.xs > gridSize or b.xs < 0):
            print("Param Error for block: ", b.id, "\nX out of bounds [", b.xs, "] expected [0-", gridSize, "]")
        if(b.ys > gridSize or b.ys < 0):
            print("Param Error for block: ", b.id, "\nY out of bounds [", b.ys, "] expected [0-", gridSize, "]")
        if(b.zs > gridSize or b.zs < 0):
            print("Param Error for block: ", b.id, "\nZ out of bounds [", b.zs, "] expected [0-", gridSize, "]")

    #Then validate no overlap
    for b in blocks:
        for bb in blocks:
            if(b.xs == bb.xs and b.ys == bb.ys and b.zs == bb.zs and b.id != b.id):
                print("Grid Error: Block [", b.id, "] has the same coordinates as Block [",bb.id,"]")
    

def arrayOfBlocks(blocks):
    arr = np.zeros(shape=(len(blocks), 3))
    for i in range(len(blocks)):
        b = blocks.pop()
        arr[i] = [b.xs,b.ys,b.zs]
    return arr

def arrayForMaze(blocks, n):
    gridSize = n
    arr = [[[0 for i in range(gridSize)] for i in range(gridSize)] for i in range(gridSize)]
    for b in blocks:
        arr[b.xs][b.ys][b.zs] = 1
    return arr

    b1 = Block("one",1,1,1)
    b2 = Block("two",2,2,2)
    arr = arrayForMaze([b1,b2], gridSize)
    for i in range(gridSize):
                for j in range(gridSize):
                    print("[", end='')
                    for k in range(gridSize):
                        print(arr[i][j][k], end=', ')
                    print("], ", end='')
                print()


def printListOfBlocks(blocks):
    for b in blocks:
        crit = "None"
        if b.critical is not None:
            crit = b.critical.id
        print("ID: ", b.id, "XYZ: [", b.xs, ",", b.ys, ",",b.zs, "] Crit:", crit, " Depth:", b.depth, "Orientation:", b.orientation, "Rotation:", b.rotation, "StrongLinked?:", b.strongLink)

def printSimpleListOfBlocks(blocks):
    for b in blocks:
        crit = "None"
        if b.critical is not None:
            crit = b.critical.id
        print("ID: ", b.id, "XYZ: [", b.xs, ",", b.ys, ",",b.zs, "] Crit:", crit, " Depth:", b.depth)

def getBlockFromCoords(blocks, x, y, z):
    for b in blocks:
        if b.xs == x and b.ys == y and b.zs == z:
            return b
    else:
        return None

def getStartingBlocks(blocks):
    starters = []
    for b in blocks:
        if b.ys == 0:
            starters.append(b)
    return starters