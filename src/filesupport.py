import block


#Take list of Blocks and filename and prints to file
def printToFile(blocks, fileName):
    blockID = 0
    with open(fileName, 'w') as f:
        for b in blocks:
            st = str(blockID), int(b.xs), int(b.ys), int(b.zs)
            f.write(str(st))
            f.write('\n')
            blockID +=1

#Takes file name and returns list of blocks from file (Syntax from method above)
def readFromFile(fileName):
    newBlocks = []
    f = open(fileName, 'r')
    content = f.readlines()
    odd = True
    for c in content:
        # print(c.split('\''))
        cout = c.split('\'')
        numCout = cout[2].split(",")
        # Pull info from file
        b = block.Block(cout[1], int(numCout[1]), int(numCout[2]), int(numCout[3].split(')')[0]))
        if b is not None:
            newBlocks.append(block.Block(cout[1], int(numCout[1]), int(numCout[2]), int(numCout[3].split(')')[0])))
        #printBlocks(newBlocks)
    return newBlocks