import numpy as np

gridSize = 10

class Block:
    def __init__(self, id, xs, ys, zs):
        self.id = id
        self.xs = xs
        self.ys = ys
        self.zs = zs
    def toString(self):
        print("ID: ", self.id, " X: ", self.xs, " Y: ", self.ys, " Z: ", self.zs)
    def asArray(self):
        return [self.xs,self.ys,self.zs]
    
def validateBlocks(blocks):
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

def arrayForMaze(blocks):
    arr = [[[0 for i in range(gridSize)] for i in range(gridSize)] for i in range(gridSize)]
    for b in blocks:
        arr[b.xs][b.ys][b.zs] = 1
    return arr

    b1 = Block("one",1,1,1)
    b2 = Block("two",2,2,2)
    arr = arrayForMaze([b1,b2])
    for i in range(gridSize):
                for j in range(gridSize):
                    print("[", end='')
                    for k in range(gridSize):
                        print(arr[i][j][k], end=', ')
                    print("], ", end='')
                print()