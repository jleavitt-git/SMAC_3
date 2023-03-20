import block
import edgeGraph as eg
import filesupport as fs
import bfsDepths as bfs

MAXWEIGHT =  10

'''
Start on the bottom and work upwards
for each block, find all blocks with dependant back to that block

If dependants is higher than *Enter weight*, throw error and exit

This essentially just checks depth value
'''

def testWeight(blocks, graph):
    startingBlocks = block.getStartingBlocks(blocks)
    for b in startingBlocks:
        weightReverseDFS(b, blocks, graph)

def weightReverseDFS(b, g):
    weight = 0
    for bl in g.edges(b):
        #If a neighbor depends on b, follow the chain
        if bl.critical is not None:
            if bl.critical.id == b.id:
                weight+=weightReverseDFS(bl, g)

    #If weight it still zero then this block has no dependants and sits by by itself
    if weight == 0:
        return 1
    elif weight > MAXWEIGHT:
        #Error, this block has too many dependants
        print("[Error] Block structure failed because max weight was exceeded for block ID:", b.id)
        exit(2)
    else:
        print("Block ", b.id, " has weight: ", weight)
        return weight+1

def main():
    blocks = fs.readFromFile('struct.txt')
    g = eg.buildGraph(blocks)
    blocks = bfs.betterDepthBuilder(g, blocks)
    testWeight(blocks, g)
    print("Weight testing complete. Structure is sound.")

if __name__ == "__main__":
    main()