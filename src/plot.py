# Import libraries
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import edgeGraph as eg
from block import Block
#Params
gridSize = 10

# class Block:
#     def __init__(self, id, xs, ys, zs):
#         self.id = id
#         self.xs = xs
#         self.ys = ys
#         self.zs = zs
#     def toString(self):
#         print("ID: ", self.id, " X: ", self.xs, " Y: ", self.ys, " Z: ", self.zs)
#     def asArray(self):
#         return [self.xs,self.ys,self.zs]

# def validateBlocks(blocks):
#     #First validate each block coordinates individually
#     for b in blocks:
#         if(b.xs > gridSize or b.xs < 0):
#             print("Param Error for block: ", b.id, "\nX out of bounds [", b.xs, "] expected [0-", gridSize, "]")
#         if(b.ys > gridSize or b.ys < 0):
#             print("Param Error for block: ", b.id, "\nY out of bounds [", b.ys, "] expected [0-", gridSize, "]")
#         if(b.zs > gridSize or b.zs < 0):
#             print("Param Error for block: ", b.id, "\nZ out of bounds [", b.zs, "] expected [0-", gridSize, "]")

#     #Then validate no overlap
#     for b in blocks:
#         for bb in blocks:
#             if(b.xs == bb.xs and b.ys == bb.ys and b.zs == bb.zs and b.id != b.id):
#                 print("Grid Error: Block [", b.id, "] has the same coordinates as Block [",bb.id,"]")

# def arrayOfBlocks(blocks):
#     arr = np.zeros(shape=(len(blocks), 3))
#     for i in range(len(blocks)):
#         b = blocks.pop()
#         arr[i] = [b.xs,b.ys,b.zs]
#     return arr

# #Axis data: 1-X 2-Y 3-Z
# def axisData(blocks, axis):
#     arr = np.zeros(len(blocks))
#     if axis == 1:
#         for i in range(len(blocks)):
#             arr[i] = blocks[i].xs
#     elif(axis == 2):
#         for i in range(len(blocks)):
#             arr[i] = blocks[i].ys
#     elif(axis == 3):
#         for i in range(len(blocks)):
#             arr[i] = blocks[i].zs
#     return arr

# def axisDataNA(blocks, axis):
#     arr = []
#     if axis == 1:
#         for b in blocks:
#             arr.append(b.xs)
#     elif(axis == 2):
#         for b in blocks:
#             arr.append(b.ys)
#     elif(axis == 3):
#         for b in blocks:
#             arr.append(b.zs)
#     return arr

# def buildStruct(blocks):
#     #DFS on adjacency graph
#     #TODO something is broken... dfs not working correctly or not returning the list in order
#     if blocks is not []:
#         g = buildGraph(blocks)
#     else:
#         return None
#     completeStructs = []
#     for b in blocks:
#         if b.ys == 1:
#             for neighbor in g.edges(b):
#                 visited = set() # Set to keep track of visited nodes.
#                 dfs(visited, g, b)
#                 if len(visited) == len(blocks):
#                     completeStructs.append(visited)
#     for st in completeStructs:
#         print(list(map(lambda e : e.id, st)))

# def dfs(visited, g, b):
#     #Pick an adjacent block, place it and move, continue until no more adjacent blocks
#     for neighbor in g.edges(b):
#         if neighbor not in visited:
#             visited.add(neighbor)
#             dfs(visited, g, neighbor)
#             return


# def buildGraph(blocks):
#     #Create adjacencies
#     #Traverse dictionary and check adjacensies
#     g = Graph()
#     d = buildDic(blocks)
#     for b in blocks:
#         g.add_vertex(b)
#         adj = getNeighbors(d, b)
#         if adj != []:
#             for a in adj:
#                 if a not in g.edges(b):
#                     g.add_edge([b,a])
#     # for vertice in g:
#     #     print(f"Edges of vertice {vertice.id}: ", list(map(lambda e : e.id, g.edges(vertice))))
                
#     return g

# def buildDic(blocks):
#     #creates a dictionary of KEY:coordinates to VALUE:blocks
#     #blocks should be validated before hand so duplicate checking is not necessary
#     bDict = {}
#     for b in blocks:
#         bDict.update({(b.xs,b.ys,b.zs):b})
#     return bDict

# def getNeighbors(d, b):
#     neighbors = []
#     #Check 6 directions
#     temp = d.get((b.xs-1,b.ys,b.zs))
#     if(temp is not None):
#         neighbors.append(temp)
#     temp = d.get((b.xs+1,b.ys,b.zs))
#     if(temp is not None):
#         neighbors.append(temp)
#     temp = d.get((b.xs,b.ys-1,b.zs))
#     if(temp is not None):
#         neighbors.append(temp)
#     temp = d.get((b.xs,b.ys+1,b.zs))
#     if(temp is not None):
#         neighbors.append(temp)
#     temp = d.get((b.xs,b.ys,b.zs-1))
#     if(temp is not None):
#         neighbors.append(temp)
#     temp = d.get((b.xs,b.ys,b.zs+1))
#     if(temp is not None):
#         neighbors.append(temp)
    
#     return neighbors
    
def main():
    plt.interactive(False)

    #SampleData
    b1 = Block("one",5,1,5)
    b2 = Block("two",5,2,5)
    b3 = Block("three",5,3,5)
    b4 = Block("four",5,4,5)
    b5 = Block("five",4,1,5)
    blocks = [b1,b2,b3,b4,b5]

    #Run Validations
    b1.validateBlocks(blocks)
    g = eg.buildStruct(blocks) 

    # Plot figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #Plot data
    ax.scatter3D(eg.axisDataNA(blocks, 1), eg.axisDataNA(blocks, 2), eg.axisDataNA(blocks, 3), marker="s", s=700)
    
    for b in blocks:
        ax.text(b.xs,b.ys,b.zs,b.id, fontsize=6)
    #Set grid size
    ax.set_xlim(-1,gridSize)
    ax.set_ylim(-1,gridSize)
    ax.set_zlim(-1,gridSize)

    #Add axis labels
    ax.set_xlabel("X")

    ax.set_ylabel("Y")

    ax.set_zlabel("Z")

    # Voxels is used to customizations of the
    # sizes, positions and colors.
    #ax.voxels(data, facecolors=colors)

    ax.view_init(100, 0)
    plt.show()

if __name__ == "__main__":
    main()