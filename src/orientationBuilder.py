import numpy as np
import block

def buildOrientation(blocks):

    blocks = sorted(blocks, key=lambda x: x.depth, reverse=True)

    block.printListOfBlocks(blocks)

    for b in blocks:
        