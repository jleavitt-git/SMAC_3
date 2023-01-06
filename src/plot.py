# Import libraries
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import edgeGraph as eg
import block
import algo
#Params
gridSize = 10


def basicMaze():
    b1 = block.Block("one",0,0,0)
    b2 = block.Block("two",0,0,1)
    b3 = block.Block("three",1,0,1)
    b4 = block.Block("four",2,0,1)
    b5 = block.Block("five",2,1,1)
    b6 = block.Block("six",2,1,2)
    b7 = block.Block("seven",2,1,3)
    b8 = block.Block("eight",3,1,3)
    b9 = block.Block("nine",3,0,3)
    b10 = block.Block("ten",3,0,4)
    b11 = block.Block("eleven",4,0,4)
    # b13 = block.Block("thirteen",2,1,1)
    # b14 = block.Block("fourteen",2,1,2)
    # b15 = block.Block("fifteen",2,1,3)
    # b16 = block.Block("sixteen",3,1,2)
    return [b9,b2,b3,b4,b5,b6,b7,b8,b11,b10,b1]

def blocksFromFile():
    newBlocks = []
    f = open('struct.txt', 'r')
    content = f.readlines()
    odd = True
    for c in content:
        # print(c.split('\''))
        cout = c.split('\'')
        numCout = cout[2].split(",")
        # Pull info from file
        b = block.Block(cout[1], int(numCout[1]), int(numCout[2]), int(numCout[3].split(')')[0]))
        if b is not None:
            newBlocks.append(block.Block(cout[1], int(numCout[1]), int(numCout[2]), int(numCout[3].split(')')[0])))
        #printBlocks(newBlocks)
    return newBlocks
        

#Returns all blocks with y=0
def getStartingBlocks(blocks):
    starters = []
    for b in blocks:
        if b.ys == 0:
            starters.append(b)
    return starters

def getGridBounds(blocks):
    xMax = 0
    yMax = 0
    zMax = 0
    for b in blocks:
        x, y, z = b.xs, b.ys, b.zs
        if x > xMax:
            xMax = x
        if y > yMax:
            yMax = y
        if z > zMax:
            zMax = z
    #Add 1 to each for spacing
    return xMax+1, yMax+1, zMax+1

def main():
    plt.interactive(False)
    #SampleData
    # b1 = block.Block("one",5,1,5)
    # b2 = block.Block("two",5,2,5)
    # b3 = block.Block("three",5,3,5)
    # b4 = block.Block("four",5,4,5)
    # b5 = block.Block("five",4,1,5)
    # blocks = [b1,b2,b3,b4,b5]

    #blocks = basicMaze()
    blocks = blocksFromFile()

    #Run Validations
    block.validateBlocks(blocks, gridSize)
 
    #NOTE: Removing maze for now, not really needed
    # for b in getStartingBlocks(blocks):
    #     print("Trying block:", b.id)
    #     if algo.solveMaze(block.arrayForMaze(blocks, gridSize), gridSize, len(blocks), b.xs, b.ys, b.zs):
    #         break
    #     else:
    #         print("Solution not found...")

    g = eg.buildGraph(blocks)

    #Validate no floating blocks
    for b in blocks:
        neighbors = g.edges(b)
        if len(neighbors) == 0 and b.ys != 0:
            print("Structure Error: ", b.id, " is floating")

    peaks = eg.getPeaks(blocks)
    for p in peaks:
        eg.buildCriticals(g, p, [])
    eg.buildDepths(blocks)
    block.printListOfBlocks(blocks)

    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Plot data
    ax.scatter3D(eg.axisDataNA(blocks, 1), eg.axisDataNA(blocks, 2), eg.axisDataNA(blocks, 3), marker="s", s=700)
    
    for b in blocks:
        ax.text(b.xs,b.ys,b.zs,b.id, fontsize=6)
    #Set grid size
    gx, gy, gz = getGridBounds(blocks)
    ax.set_xlim(-1,gx)
    ax.set_ylim(-1,gy)
    ax.set_zlim(-1,gz)

    #Add axis labels
    ax.set_xlabel("X")

    ax.set_ylabel("Y")

    ax.set_zlabel("Z")

    # Voxels is used to customizations of the
    # sizes, positions and colors.
    #ax.voxels(data, facecolors=colors)

    ax.view_init(100, 0)
    plt.show()

def printBlocks(blocks):
    for b in blocks:
        print("ID: ", b.id, " X: ", b.xs, " Y: ", b.ys, " Z: ", b.zs)

if __name__ == "__main__":
    main()