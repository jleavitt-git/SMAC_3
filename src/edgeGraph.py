from block import Block
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

def main():
    print(1)

if __name__ == "__main__":
    main()