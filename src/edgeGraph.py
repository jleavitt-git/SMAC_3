import block
import numpy as np
from graph import Graph

def axisData(blocks, axis):
    arr = np.zeros(len(blocks))
    if axis == 1:
        for i in range(len(blocks)):
            arr[i] = blocks[i].xs
    elif(axis == 2):
        for i in range(len(blocks)):
            arr[i] = blocks[i].ys
    elif(axis == 3):
        for i in range(len(blocks)):
            arr[i] = blocks[i].zs
    return arr

def axisDataNA(blocks, axis):
    arr = []
    if axis == 1:
        for b in blocks:
            arr.append(b.xs)
    elif(axis == 2):
        for b in blocks:
            arr.append(b.ys)
    elif(axis == 3):
        for b in blocks:
            arr.append(b.zs)
    return arr

    
def buildStruct(blocks):
    #DFS on adjacency graph
    if blocks is not []:
        g = buildGraph(blocks)
    else:
        return None
    completeStructs = []
    for b in blocks:
        if b.ys == 1:
            for neighbor in g.edges(b):
                visited = set() # Set to keep track of visited nodes.
                dfs(visited, g, b)
                if len(visited) == len(blocks):
                    completeStructs.append(visited)
    # for st in completeStructs:
    #     print(list(map(lambda e : e.id, st)))
    return completeStructs

def dfs(visited, g, b):
    #Pick an adjacent block, place it and move, continue until no more adjacent blocks
    for neighbor in g.edges(b):
        if neighbor not in visited:
            visited.add(neighbor)
            dfs(visited, g, neighbor)
            return

def buildGraph(blocks):
    #Create adjacencies
    #Traverse dictionary and check adjacensies
    g = Graph()
    d = buildDic(blocks)
    for b in blocks:
        g.add_vertex(b)
        adj = getNeighbors(d, b)
        if adj != []:
            for a in adj:
                if a not in g.edges(b):
                    g.add_edge([b,a])
    # for vertice in g:
    #     print(f"Edges of vertice {vertice.id}: ", list(map(lambda e : e.id, g.edges(vertice))))
                
    return g

def buildDic(blocks):
    #creates a dictionary of KEY:coordinates to VALUE:blocks
    #blocks should be validated before hand so duplicate checking is not necessary
    bDict = {}
    for b in blocks:
        bDict.update({(b.xs,b.ys,b.zs):b})
    return bDict

# d: Dictionary, b: block
def getNeighbors(d, b):
    neighbors = []
    #Check 6 directions
    temp = d.get((b.xs-1,b.ys,b.zs))
    if(temp is not None):
        neighbors.append(temp)
    temp = d.get((b.xs+1,b.ys,b.zs))
    if(temp is not None):
        neighbors.append(temp)
    temp = d.get((b.xs,b.ys-1,b.zs))
    if(temp is not None):
        neighbors.append(temp)
    temp = d.get((b.xs,b.ys+1,b.zs))
    if(temp is not None):
        neighbors.append(temp)
    temp = d.get((b.xs,b.ys,b.zs-1))
    if(temp is not None):
        neighbors.append(temp)
    temp = d.get((b.xs,b.ys,b.zs+1))
    if(temp is not None):
        neighbors.append(temp)
    
    return neighbors

#Returns all blocks at highest level
def getPeaks(blocks):
    peaks = []
    maxHeight = 0
    for b in blocks:
        if b.ys > maxHeight:
            maxHeight = b.ys
    for b in blocks:
        if b.ys == maxHeight:
            peaks.append(b)
    return peaks


#DFS adds critical nodes to each block
def buildCriticals(g, b, visited):
    visited.append(b)
    neighbors = g.edges(b)
    for n in neighbors:
        if n.critical is None and n.ys != 0 and not visited.__contains__(n):
            buildCriticals(g, n, visited)
    findCritical(g, b)
        
def findCritical(g, b):
    neighbors = g.edges(b)
    #on the floor
    if b.ys == 0:
        return b
    #n is below b
    for n in neighbors:
        if n.ys < b.ys:
            b.critical = n
            b.depth = n.depth+1
            return b
    #n is next to b, find one with shorted depth
    possibleCrits = []
    for n in neighbors:
        if n.ys == b.ys:
            possibleCrits.append(n)
    smallestDepth = 100000000 #outside possible depth
    for p in possibleCrits:
        if p.depth < smallestDepth:
            smallestDepth = p.depth
    if smallestDepth != 100000000:
        for n in neighbors:
            if smallestDepth == n.depth:
                b.critical = n
                b.depth = n.depth+1
                return b
    #n is above b and b is floating
    else:
        for n in neighbors:
            if n.ys == b.ys+1:
                b.critical = n
                b.depth = n.depth+1
    return b


            


def main():
    #SampleData
    b1 = block.Block("one",5,0,5)
    b2 = block.Block("two",5,1,5)
    b3 = block.Block("three",5,2,5)
    b4 = block.Block("four",5,3,5)
    b5 = block.Block("five",4,0,5)
    blocks = [b1,b2,b3,b4,b5]
    print(1)
    g = buildGraph(blocks)
    buildCriticals(g, blocks[3], [])
    block.printListOfBlocks(blocks)

if __name__ == "__main__":
    main()