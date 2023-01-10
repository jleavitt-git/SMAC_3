import numpy as np
import block

#DFS adds critical nodes to each block
def buildCriticals(g, b, visited):
    visited.append(b)
    neighbors = g.edges(b)
    for n in neighbors:
        if n.critical is None and n.ys != 0 and not visited.__contains__(n):
            buildCriticals(g, n, visited)
    finedCritical(g, b)
        
def findCritical(g, b):
    neighbors = g.edges(b)
    #on the floor
    if b.ys == 0:
        return b
    #n is below b and not supported by ground
    for n in neighbors:
        if n.ys < b.ys and n.critical != b:
            b.critical = n
            b.depth = n.depth+1
            return b
    #n is next to b, find one with shorted depth
    for n in neighbors:
        if n.ys == b.ys and n.critical is not b:
            b.critical = n
            b.depth = n.depth+1
            return b
    #n is above b and b is floating
    for n in neighbors:
        if n.ys == b.ys+1:
            b.critical = n
            b.depth = n.depth+1
    return b

def finedCritical(g, b):
    neighbors = g.edges(b)

    #Block is on the floor
    if b.ys == 0:
        return b
    
    #Block is sitting on a pillar
    for n in neighbors:
        if n.ys == b.ys-1 and isPillar(g, n):
            b.critical = n
            b.depth = n.depth+1
            return b
        
    #Block has adjacent stable blocks
    for n in neighbors:
        if n.ys == b.ys and n.critical is not b:
            b.critical = n
            b.depth = n.depth+1
            return b
    
    #Block is hanging
    for n in neighbors:
        if n.ys == b.ys+1:
            b.critical = n
            b.depth = n.depth+1
    return b


def isPillar(g, b):
    #Block is on the floor
    if b.ys == 0:
        return True
    neighbors = g.edges(b)

    #If there is a block below, recurse downwards on y axis
    for n in neighbors:
        if n.ys == b.ys-1:
            return isPillar(g, n)

    #Never hit floor, is not a pillar
    return False