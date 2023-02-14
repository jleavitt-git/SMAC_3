import numpy as np
import block
import edgeGraph as eg

def buildOrientation(blocks, g):

    #Sort by depth, highest first
    blocks = sorted(blocks, key=lambda x: x.depth, reverse=True)

    # block.printListOfBlocks(blocks)

    # for b in blocks:
    #     neighbors = g.edges(b)

    #     nlen = len(neighbors)

    #     if nlen < 1:
    #         b.type = block.type.SCAFFOLD
    #         b.orientation = block.orientation.ANY
    #         b.rotation = block.rotation.ANY
    #     elif nlen < 2:
    #         b.orientation = getDirection(b, neighbors.get(0))

    return blocks


def getDirection(b, n):
    if b.xs - n.xs == 1:
        return block.orientation.X
    elif n.xs - b.xs == 1:
        return block.orientation.XN
    if b.ys - n.ys == 1:
        return block.orientation.Y
    elif n.ys - b.ys == 1:
        return block.orientation.YN
    if b.zs - n.zs == 1:
        return block.orientation.Z
    elif n.zs - b.zs == 1:
        return block.orientation.ZN
    else:
        print("Error: Unknown direction on block, " + b.id)
    return blocks
