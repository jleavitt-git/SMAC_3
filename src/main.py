# Import libraries
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import edgeGraph as eg
import block
import filesupport as fs
import plot
import bfsOrientation as ob

#Params
gridSize = 10

#Returns all blocks with y=0
def getStartingBlocks(blocks):
    starters = []
    for b in blocks:
        if b.ys == 0:
            starters.append(b)
    return starters


def main():
    #Run the sym to get structure if wanted
    doSim = input("Run simulation for new structure? [y/n]:")
    if doSim == "y" or doSim == "Y":
        os.system('python3 sim.py')

    #import blocks from structure
    blocks = fs.readFromFile('struct.txt')

    #Basic block validations
    block.validateBlocks(blocks, gridSize)
 
    #Build edge graph to find block neighbors
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
   

    # orderedBlocks = None
    # for b in getStartingBlocks(blocks):
    #     print("Trying block:", b.id)
    #     orderedBlocks = dfs.doDFS(g, b, len(blocks))
    #     if orderedBlocks is not None:
    #         break
    #     else:
    #         print("Solution not found...")
    # # orderedBlocks = None
    # # for b in getStartingBlocks(blocks):
    # #     print("Trying block:", b.id)
    # #     orderedBlocks = algo.solveMaze(block.arrayForMaze(blocks, gridSize), gridSize, len(blocks), b.xs, b.ys, b.zs, blocks)
    # #     if orderedBlocks is not None:
    # #         break
    # #     else:
    # #         print("Solution not found...")
   

    # ob.buildOrientation(blocks, g)

    #blocks = cdfs.initFancyDFS(blocks, g)

    # blocks = sorted(blocks, key=lambda b: b.depth if b.depth is not None else 0, reverse=False)

    # block.printListOfBlocks(blocks)


    # gv.buildGraph(blocks)
   
    #block.printListOfBlocks(blocks)
    blocks = ob.attemptOrientation(g, blocks)

    block.printListOfBlocks(blocks)

    # Plot figure
    plt.interactive(False)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Plot data
    ax.scatter3D(eg.axisDataNA(blocks, 1), eg.axisDataNA(blocks, 2), eg.axisDataNA(blocks, 3), marker="s", s=700)
    
    for b in blocks:
        ax.text(b.xs,b.ys,b.zs,b.id, fontsize=6)
    #Set grid size
    gx, gy, gz = plot.getGridBounds(blocks)
    ax.set_xlim(-1,gx)
    ax.set_ylim(0,gy)
    ax.set_zlim(-1,gz)

    #Add axis labels
    ax.set_xlabel("X")

    ax.set_ylabel("Y")

    ax.set_zlabel("Z")

    ax.view_init(100, 0)
    plt.show()

if __name__ == "__main__":
    main()