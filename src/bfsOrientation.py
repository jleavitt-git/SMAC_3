import block
import edgeGraph as eg
import bfsDepths as bfs

#Returns all blocks with y=0
def getStartingBlocks(blocks):
    starters = []
    for b in blocks:
        if b.ys == 0:
            starters.append(b)
    return starters

def attemptOrientation(g, blocks):
    blocks = sorted(blocks, key=lambda x: x.depth)

    '''
    Start on the ground, go up until there is a horizontal neighbor not on a pillar
    
    Find shortest path to ground not from the traversed pillar

    Find a way to not go back down a directly adjacent pillar (Ex. a 2x2 pillar)

    Allow overhangs of 4 blocks, afterwards needs pillar within 4 blocks

    How can I use the criticals to my advantage here?
    
    '''

    for b in blocks:
        if b.ys == 0:
            b.orientation = block.orientation.YN
        if b.ys > 0:
            b.orientation = getDirection(b, b.critical)
            # print(f"block {b.id} is at orientation {b.orientation}")

    return blocks



def getDirection(b, n):
    if b.xs - n.xs == 1:
        return block.orientation.XN
    elif n.xs - b.xs == 1:
        return block.orientation.X
    elif b.ys - n.ys == 1:
        return block.orientation.YN
    elif n.ys - b.ys == 1:
        return block.orientation.Y
    elif b.zs - n.zs == 1:
        return block.orientation.ZN
    elif n.zs - b.zs == 1:
        return block.orientation.Z
    else:
        print("Error: Unknown direction on block, " + b.id)