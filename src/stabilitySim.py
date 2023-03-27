import block
import edgeGraph as eg
import weightSim as ws
from ValidationSupport import ValidationFailure, ValidationLog
'''
Build by depth
Every time a block is placed, check for overhang.
    If overhang (Could be multiple height overhang), ensure strong joints back to a pillar
    If not strong joint, check if block has been hard assigned. If so, fail
        Else take hard assignment from pillar
    

On Completion
    Basic weight checks for soft joints (Only allow 1 blocks overhang soft joints)

See where it goes.
 '''

OVERHANG = 3

# def testStability(blocks, g):
#     blocks = sortByDepth(blocks)

#     for b in blocks:
#         if b.ys == 0:
#             #Ground, always dowwards pin
#             b.orientation = block.orientation.YN
#         neighbors = g.edges(b)
#         for n in neighbors:
#             #There is block below
#             if n.ys == b.ys-1:
#                 #Check if pillar, else hanging block
#                 if not isPillar(n):
#                     #Check surroundings for priority else strong link hanging block
#                     nothing = 1
#             #Break once b has orientation and face
                
# def prioritzeOrientation(blocks, g):
#     blocks = sortByDepth(blocks)

#     #Strong link is set to True when it's pin is set into a block

#     for b in blocks:
#         if b.ys == 0:
#             #Floor, no logic here needed
#             print("Floor", b.id)
#             b.rotation = block.orientation.Y
#             b.strongLink = True
#             continue
#         if b.strongLink is not None:
#             print("repeat loop", b.id, "Strong", b.strongLink)
#             #Block has already been weak Linked, leave it
#             continue
#         neighbors = g.edges(b)
#         numDependants = 0
#         for n in neighbors:
#             if n.critical == b:
#                 #find number of dependants
#                 numDependants+=1
#         if numDependants == 0:
#             #No dependants, check for overhang / bridge
#             # b.rotation = block.orientation.ANY
#             dir = getOppositeOrientation(b)
#         elif numDependants == 1:
#             for n in neighbors:
#                 if n.critical is not None:
#                     if n.critical == b:
#                         print("one dependant", b.id)
#                         #Set rotation of single dependant
#                         # rot = getRotation(b, n)
#                         # for f in blocks:
#                         #     if f.id == n.id:
#                         #         f.rotation = rot
#                         setRotation(b, n)
#                         b.strongLink = True
#         else:
#             #Find weight of each dependant, link to highest
#             highID = getHeaviestBlock(b, g)
#             needWeak = True
#             if highID == "":
#                 print("Error...")
#                 exit(1)
#             for f in blocks:
#                 if f.id == highID:
#                     setRotation(f, n)
#                     f.strongLink = True
#                     needWeak = False
#                     break
#             if needWeak:
#                 for f in blocks:
#                     if f.id == highID:
#                         #Block must be weak linked
#                         weight = ws.weightReverseDFS(f, g)
#                         if weight > 1:
#                             print(f"Error: Weak link block ID:[{f.id}] is overweight limitations, exiting...")
#                             exit(1)
#                         else:
#                             #print("Not too heavy", b.id)
#                             f.strongLink = False
#                             f.orientation = block.orientation.ANY
#                             f.rotation = block.orientation.ANY
#         #Now check overhang and weight
#         overhang = 0
#         b.pathToGround.reverse()
#         for p in b.pathToGround:
#            if p.id == b.id:
#                continue
#            if not isPillar(g, p):
#                overhang+=1
#            else:
#                #print(f"Overhang for {b.id} is {overhang}")
#                break
#         if overhang > OVERHANG:
#             print("Error: Overhang over 4 blocks detected for block:", b.id)
#             string = "Block path"
#             for l in b.pathToGround:
#                 string+= f" | {l.id}"
#             print(string)
#             exit(1)
        

'''
Classify each block:
    Floor: 1
    Pillar: 2
    Corner: 3
    Overhang: 4
    Hanging: 5
    Stacked on Overhang: 6
    Other: 7
'''
def POV2(blocks, g):
    blocks = sortByDepth(blocks)

    for b in blocks:
        bClass = classifyBlock(b, g)
        print(f"Block {b.id} is class {bClass}")
        if bClass == 1:
            #Floor logic
            print("Floor", b.id)
            b.rotation = block.orientation.Y
            b.strongLink = True
        elif bClass == 2:
            #Pillar Logic
            for n in g.edges(b):
                if n.ys == b.ys+1:
                    #Has block above
                    b.rotation = block.orientation.Y
            #No block above, set to any
            b.rotation = block.orientation.ANY
            b.strongLink = True
            
            neighbors = g.edges(b)


            if len(neighbors) == 2 and b.rotation == block.orientation.ANY:
                for n in neighbors:
                    if n != b.critical:
                        # print(f"Block {b.id} rotating to {n.id}")
                        setRotation(b, n)
        elif bClass == 3:
            #Corner Logic
            dependants = 0
            for n in g.edges(b):
                if n.critical is not None:
                    if n.critical == b:
                        dependants+=1
            if dependants == 1:
                #Only one dependant, link
                print("one dependant", b.id)
                setRotation(b, n)
                b.strongLink = True
            elif dependants > 1:
                #Pick heaviest block and strong link to it
                heav = getHeaviestBlock(b, blocks, g)
                if heav == "":
                    print(f"Code Error: No dependants found for {b.id} for heaviest block choice")
                    exit(1)
                else:
                    deps = getDependants(b, g)
                    for f in blocks:
                        if f.id == heav:
                            setRotation(b, f)
                            b.strongLink = True
                        else:
                            for d in deps:
                                if f.id == d.id:
                                    weight = ws.weightReverseDFS(d, blocks, g)
                                    if weight > 1:
                                        deps = getDependants(f, g)
                                        deps = deps + f.pathToGround
                                        f.pathToGround = deps
                                        ValidationFailure(f, blocks, ValidationLog.WEAK_LINK_FAIL)
                                    else:
                                        #print("Not too heavy", f.id)
                                        f.strongLink = False
                                        f.orientation = block.orientation.ANY
                                        f.rotation = block.orientation.ANY
            else:
                #No dependants
                b.rotation = block.orientation.ANY
                b.strongLink = True

        elif bClass == 4:
            #Overhang Logic
            deps = getDependants(b, g)
            if b.strongLink == False:
                #Already been weak linked
                pass
            elif len(deps) == 0 and b.critical.rotation == getOppositeOrientation(b, blocks):
                b.rotation = block.orientation.ANY
                b.strongLink = True
            #If dependant is corner and not rotated towards it, weak link it
            elif b.critical.rotation != getOppositeOrientation(b, blocks):
                b.rotation = block.orientation.ANY
                b.strongLink = False
                continue
            else:
                if len(deps) == 1:
                    setRotation(b,deps[0])
                    b.strongLink = True

                else:
                    pBlock = findPriorityBlock(b, blocks, g)
                    for f in blocks:
                        if f.id == pBlock.id:
                            setRotation(b, f)
                            b.strongLink == True
                    #Bridge logic on X
            #Check neighbor for also overhang but not dependant on same axis, then build bridge
                #Add clause for only one other neighbor, could be an 90 degree bridge. Ignore other cases

            neighbors = g.edges(b)
            if len(neighbors) == 2:
                for n in neighbors:
                    if n != b.critical and b.rotation == block.orientation.ANY:
                        setRotation(b, n)

            dist = distFromPillar(b, g)
            if dist > OVERHANG:
                ValidationFailure(b, blocks, ValidationLog.OVERHANG_FAIL, overhang=OVERHANG)
        elif bClass == 5:
            #Hanging Logic

            #These will always weak link for now
            
            #Write method to find distance from pillar, more than 2 means impossible to build
            dist = distFromPillar(b, g)
            if dist > 2:
                print("Error: Distance from pillar for block {b.id} is too large, cannot be placed")
                exit(1)
            else:
                b.orientation = block.orientation.ANY
                b.rotation = block.rotation.ANY
                b.strongLink = False

        elif bClass == 6:
            #Sitting on Overhang Logic
            for n in g.edges(b):
                if b.critical == n:
                    if n.rotation == block.orientation.Y and n.strongLink == True:
                        #Block below has strong jointed upwards, so we can link
                        b.rotation = block.orientation.ANY
                        b.strongLink == True
                        continue
            pBlock = findPriorityBlock(b, blocks, g)
            if pBlock is None:
                #No dependants, vibe
                b.rotation = block.orientation.ANY
                b.strongLink = True
            else:
                for n in g.edges(b):
                    if n.id == pBlock.id:
                        setRotation(b, n)
                        b.strongLink = True

            #If block below is overhang and has adjacent dependants, try to strong link upwards, else sideways

        else:
            #Other, logic some undefined behavior
            print(f"No classification found for block {b.id}, exiting")
            exit(1)

    for b in blocks:
        if not b.strongLink:
            for f in blocks:
                if f.critical is not None:
                    if f.critical is b:
                        print(f"Error: Weak Link block {b.id} has dependants that can't be supported.")
                        exit(1)

'''
Floor: 1
Pillar: 2
Corner: 3
Overhang: 4
Hanging: 5
Stacked on Overhang: 6
Other: 7
'''
def classifyBlock(b, g):
    if b.ys == 0:
        return 1
    elif isPillar(g, b):
        #Check if corner
        for n in g.edges(b):
            #see if adjacent blocks are dependant
            if n.critical is not None:
                if n.critical == b and n.ys == b.ys:
                    #Contains adjacent block that is dependant on this one, so must be corner
                    return 3
        #No adjacent dependant blocks, so just a pillar
        return 2
    else:
        ret = sittingOnOverhang(b, b, g)
        if ret == 1:
            return 6
        elif ret == 2:
            return 4
        

'''
Params:
ob: Original block
b: initial input will have same b as OB, this is the recursion block
g: edgeGraph

Pillar: 0
Sitting on Overhang: 1
IS the overhang: 2
'''
def sittingOnOverhang(ob, b, g):
    #if it hits the floor, not sitting on overhang
    if b.ys == 0:
        return 0
    for n in g.edges(b):
        if n.ys == b.ys-1:
            if n.critical is not None:
                if n.critical == b and ob.ys - n.ys == 1:
                    #Block below is hanging, so this block IS the overhang
                    return 2
                else:
                    #Block below is not hanging, so sit on overhang
                    return 1
    
    #No neighbors below that aren't hanging and not floor, must be overhang
    return 2
        

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

def sortByDepth(blocks):
    return sorted(blocks, key=lambda x: x.depth, reverse=False)

#deprecated
def setPRotation(b, n):
    #Here, we assume the ORIENTATION attribute for n is set towards b
    if n.orientation == block.orientation.Y:
        b.rotation = block.orientation.YN
    elif n.orientation == block.orientation.YN:
        b.rotation = block.orientation.Y
    elif n.orientation == block.orientation.X:
        b.rotation = block.orientation.XN
    elif n.orientation == block.orientation.XN:
        b.rotation = block.orientation.X
    elif n.orientation == block.orientation.Z:
        b.rotation = block.orientation.ZN
    elif n.orientation == block.orientation.ZN:
        b.rotation = block.orientation.Y

def setRotation(b, n):
    if b.xs == n.xs+1:
        b.rotation = block.orientation.XN
    elif b.xs == n.xs-1:
        b.rotation = block.orientation.X
    if b.ys == n.ys+1:
        b.rotation = block.orientation.YN
    elif b.ys == n.ys-1:
        b.rotation = block.orientation.Y
    if b.zs == n.zs+1:
        b.rotation = block.orientation.ZN
    elif b.zs == n.zs-1:
        b.rotation = block.orientation.Z

def getOppositeOrientation(b, blocks):
    print(f"{b.id} : {b.orientation}")
    if(b.orientation > 0):
        return block.orientation((int(b.orientation) + 3)%6)
    else:
        #This should not hit because the bfs orientation is run first
        print(f"Error, no orientation found for {b.id}")
        ValidationFailure(b, blocks, ValidationLog.DEBUG)

def getHeaviestBlock(b, blocks, g):
    dependants = []
    maxWeight = -1
    heaviestID = ""
    neighbors = g.edges(b)
    for n in neighbors:
        if n.critical is not None:
            if n.critical == b:
                dependants.append(n)
    for d in dependants:
        weight = ws.weightReverseDFS(d, blocks, g)
        if weight > maxWeight:
            maxWeight = weight
            heaviestID = d.id
    print(f"Returning heavy {heaviestID}")
    return heaviestID

def getDependants(b, g):
    deps = []
    for n in g.edges(b):
        if n.critical is not None:
            if n.critical == b:
                deps.append(n)
    return deps

def distFromPillar(b, g):
    ptg = b.pathToGround
    ptg.reverse()
    for p in ptg:
        if isPillar(g, p):
            xDiff = abs(b.xs - p.ys)
            yDiff = abs(b.ys - p.ys)
            return min(xDiff, yDiff)
    print(f"Error: No pillar found for block {b.id}")
    exit(1)

def findPriorityBlock(b, blocks, g):
    #Find block that needs strong joint the most:
        #Heaviest horizontal dependant first
        #Then up if exists, otherwise down if exists
    deps = getDependants(b, g)
    hDeps = []
    aboveDeps = []
    belowDeps = []
    for d in deps:
        if abs(d.xs - b.xs) == 1 or abs(d.zs - b.zs) == 1:
            #Horizontal Dependant
            hDeps.append(d)
        elif d.ys == b.ys-1:
            belowDeps.append(d)
        elif d.ys == b.ys+1:
            aboveDeps.append(d)
        else:
            print(f"Error: Dependant {d.id} is not adjacent to {b.id}")
            exit(1)
    if len(hDeps) > 0:
        if len(hDeps) == 1:
            return hDeps[0]
        else:
            for h in hDeps:
                #prioritize overhang block
                if classifyBlock(h, g) == 4:
                    return h
            heav = getHeaviestBlock(b, blocks, h)
            for f in g.edges(b):
                if f.id == heav:
                    return f
    if len(aboveDeps) > 0:
        return aboveDeps[0]
    elif len(belowDeps) > 0:
        return belowDeps[0]
    #No dependants
    return None