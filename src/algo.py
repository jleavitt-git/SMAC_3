# Python3 program to solve Rat in a Maze
# problem using backtracking

# Maze size
n = 4

# A utility function to check if x, y is valid
# index for N * N Maze


def isValid(n, maze, x, y, z, res):
    if x >= 0 and y >= 0 and z >= 0 and x < n and y < n and z < n and maze[x][y][z] == 1 and res[x][y][z] == 0:
        return True
    return False

# A recursive utility function to solve Maze problem


def DoMaze(n, maze, move_x, move_y, move_z, x, y, z, res):

    # if (x, y, z is goal) return True
    if x == n-1 and y == n-1 and z == 0:
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
            res[x_new][y_new][z_new] = 1
            if DoMaze(n, maze, move_x, move_y, move_z, x_new, y_new, z_new, res):
                return True
            res[x_new][y_new][z_new] = 0
    return False


def solveMaze(maze):

        # Creating a 4 * 4 2-D list
    res = [[[0 for i in range(n)] for i in range(n)] for i in range(n)]
    res[0][0][0] = 1

    # x matrix for each direction
    move_x = [-1, 1, 0, 0, 0, 0]

    # y matrix for each direction
    move_y = [0, 0, -1, 1, 0, 0]

    # y matrix for each direction
    move_z = [0, 0, 0, 0, -1, 1]
    
    if DoMaze(n, maze, move_x, move_y, move_z, 0, 0, 0, res):
        for i in range(n):
            for j in range(n):
                print("[", end='')
                for k in range(n):
                    print(res[i][j][k], end=', ')
                print("], ", end='')
            print()
    else:
        print('Solution does not exist')


# Driver program to test above function
if __name__ == "__main__":
    # Initialising the maze
    maze = [[[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],
        [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]]]

    solveMaze(maze)

# This code is contributed by Anvesh Govind Saxena
