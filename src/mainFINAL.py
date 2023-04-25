# Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import edgeGraph as eg
import block
import filesupport as fs
import plot
import bfsOrientation as ob
import bfsDepths as bfs
import stabilitySim as sm
import ValidationSupport
from ValidationSupport import ValidationLog
import blueprintExporter as be

#Params
gridSize = 10

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
    floatingBlocks = []
    for b in blocks:
        neighbors = g.edges(b)
        if len(neighbors) == 0 and b.ys != 0:
            floatingBlocks.append(b)

    
    blocks = bfs.betterDepthBuilder(g, blocks)

    if len(floatingBlocks) > 0:
        ValidationSupport.ValidationFailure(floatingBlocks[0], blocks, ValidationLog.FLOATING_BLOCK_ERROR)
   
    #Create baseline orientation guesses
    blocks = ob.attemptOrientation(g, blocks)

    #Complete orientation builder
    sm.POV2(blocks, g)

    #Only reach here if no validation was thrown
    plot.showFinalPlot(blocks)
    #plot.showValidationPlot(blocks)
    be.exportBlocks(blocks, g)


if __name__ == "__main__":
    main()