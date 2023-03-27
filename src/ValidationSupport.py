from enum import Enum
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import block
import plot
import edgeGraph as eg

gridSize = 10

class ValidationLog(Enum):
    DEBUG = 0
    FLOATING_BLOCK_ERROR = 1
    OVERWEIGHT = 2
    WEAK_LINK_FAIL = 3
    OVERHANG_FAIL = 4
    OUT_OF_BOUNDS = 5
    OVERLAP = 6
    IMPOSSIBLE_TO_PLACE = 7


'''
b = Block object of failure
allBlocks = list of all blocks
type = ValidationLog enum
overlap (if applicable): Block that is overlapped
weight (if applicable): Weight constant
overhang (if applicable): Overhang constant
'''
def ValidationFailure(b, allBlocks, type, overlap=None, weight=None, overhang=None):
    if type == ValidationLog.DEBUG:
        b.pathToGround = allBlocks
        pass
    
    elif type == ValidationLog.FLOATING_BLOCK_ERROR:
        print(f"[VALIDATION FAIL]: Floating block detected, Block ID: {b.id}")

    elif type == ValidationLog.OVERWEIGHT:
        if weight is None:
            print("Code error, no weight was passed")
            exit(1)
        print(f"[VALIDATION FAIL]: Block structure failed because max weight [{weight}] was exceeded, Block ID: {b.id}")

    elif type == ValidationLog.WEAK_LINK_FAIL:
        print(f"[VALIDATION FAIL]: Block is too heavy to be weak linked, Block ID: {b.id}")

    elif type == ValidationLog.OVERHANG_FAIL:
        if overhang is None:
            print("Code error, no overhang was passed")
            exit(1)
        print(f"[VALIDATION FAIL]: Block would cause an overhang over the specified maximum constraint [{overhang}], Block ID: {b.id}")

    elif type == ValidationLog.OUT_OF_BOUNDS:
        print(f"[VALIDATION FAIL]: Block placed out of bounds expected [0-{gridSize}], Block ID: {b.id}")

    elif type == ValidationLog.OVERLAP:
        if overlap is None:
            print("Code error, no overlapping block was passed")
            exit(1)
        print(f"[VALIDATION FAIL]: Two blocks have the same coordinates, Block IDs: [{b.id},{overlap.id}]")

    elif type == ValidationLog.IMPOSSIBLE_TO_PLACE:
        print(f"[VALIDATION FAIL]: Block is too far from a pillar to be placed by an inchworm, Block ID: {b.id}")
    else:
        print("Validation: Invalid type")
        exit(1)

    blocks = b.pathToGround
    if len(blocks) < 1:
        blocks = allBlocks

    block.printListOfBlocks(blocks)
    #block.printSimpleListOfBlocks(blocks)

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

    exit(1)