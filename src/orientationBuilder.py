import numpy as np
import block

def buildOrientation(blocks):

    blocks = sorted(blocks, key=lambda x: x.depth, reverse=True)

    return blocks