import block

# Maze size
n = 10

# A utility function to check if x, y is valid
# index for N * N Maze
blocks = []

def isValid(n, maze, x, y, z, res):
    if x >= 0 and y >= 0 and z >= 0 and x < n and y < n and z < n and maze[x][y][z] == 1 and res[x][y][z] == 0:
        return True
    return False

# A recursive utility function to solve Maze problem


def DoMaze(n, maze, move_x, move_y, move_z, x, y, z, res, blocksTraversed, blockCount, blocks, solvedListOfBlocks):

    # if (x, y, z is goal) return True
    # if x == n-1 and y == 0 and z == n-1:
    if blocksTraversed == blockCount-1:
        return True
    for i in range(6):
        # Generate new value of x
        x_new = x + move_x[i]

        # Generate new value of y
        y_new = y + move_y[i]

        # Generate new value of z
        z_new = z + move_z[i]

        # Check if maze[x][y] is valid
        if isValid(n, maze, x_new, y_new, z_new, res):
            # mark x, y as part of solution path
            foundBlock = block.getBlockFromCoords(blocks, x_new, y_new, z_new)
            if foundBlock in solvedListOfBlocks:
                solvedListOfBlocks.remove(foundBlock)
                solvedListOfBlocks.append(foundBlock)
            else:
                solvedListOfBlocks.append(foundBlock)
            res[x_new][y_new][z_new] = 1
            blocksTraversed+=1
            # print("Coords: [", z_new, ",", y_new, ",", z_new, "]")
            if DoMaze(n, maze, move_x, move_y, move_z, x_new, y_new, z_new, res, blocksTraversed, blockCount, blocks, solvedListOfBlocks):
                return True
            res[x_new][y_new][z_new] = 0
    return False

#Attemps to solve maze, coordinates are starting blocks
def solveMaze(maze, gridSize, blockCount, x, y, z, blocks):
    n = gridSize
    solvedListOfBlocks = [block.getBlockFromCoords(blocks, x,y,z)]
        # Creating a 4 * 4 2-D list
    res = [[[0 for i in range(n)] for i in range(n)] for i in range(n)]
    res[x][y][z] = 1

    # x matrix for each direction
    move_x = [-1, 1, 0, 0, 0, 0]

    # y matrix for each direction
    move_y = [0, 0, -1, 1, 0, 0]

    # y matrix for each direction
    move_z = [0, 0, 0, 0, -1, 1]
    
    if DoMaze(n, maze, move_x, move_y, move_z, x, y, z, res, 0, blockCount, blocks, solvedListOfBlocks):
        # for i in range(n):
        #     for j in range(n):
        #         print("[", end='')
        #         for k in range(n):
        #             print(res[i][j][k], end=', ')
        #         print("], ", end='')
        #     print()
        return solvedListOfBlocks
    else:
        # print('Solution does not exist')
        return None
        


# Driver program to test above function
if __name__ == "__main__":
    # Initialising the maze
    # maze = [[[1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    #     [[1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
    #     [[0, 0, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    #     [[1, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]]
    maze = [[[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0]]]
    print(maze[0][0][1])


    print(maze[1][0][0])
    print(maze[0][1][1])
    solveMaze(maze, 4, 9, 0, 0, 0, [])
