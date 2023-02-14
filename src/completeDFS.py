import edgeGraph as eg 
import block
import os
import filesupport as fs


gridSize = 10

#Returns all blocks with y=0
def getStartingBlocks(blocks):
    starters = []
    for b in blocks:
        if b.ys == 0:
            starters.append(b)
    return starters



def initFancyDFS(blocks, g):
    visited = []
    for s in getStartingBlocks(blocks):
        res = doDFS(s, blocks, g, visited)
        if res is not None:
            if len(res) == len(blocks):
                return res
    return None


def doDFS(n, blocks, g, visited):
    visited.append(n)
    #print("Block ", n.id, " for len ", len(visited))
    if len(visited) == len(blocks):
        return visited
    for i in g.edges(n):
        if i not in visited:
            res = doDFS(i, blocks, g, visited)
            if res is not None:
                return res
    return None


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
   
    #SampleData
    res = initFancyDFS(blocks, g)
    if res is not None:
        block.printListOfBlocks(res)
    else:
        print("no Solution")

if __name__ == "__main__":
    main()