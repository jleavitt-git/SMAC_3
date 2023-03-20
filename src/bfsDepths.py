import edgeGraph as eg
import block

def shortest_path(g, node1):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1.ys == 0:
        return path_list[0]
        
    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = g.edges(last_node)
        # Search goal node
        goalNode = block.Block(str("False"),0,0,0)
        for n in next_nodes:
            if n.ys == 0:
                goalNode = n
        if goalNode.id != "False":
            current_path.append(goalNode)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []

def betterDepthBuilder(g, blocks):
    for b in blocks:
        if b.depth == 0 and b.ys != 0:
            path = shortest_path(g, b)
            b.pathToGround = path
            path.reverse()
            for x in range(len(path)):

                if path[x].depth is 0 and path[x].ys != 0:
                    path[x].depth = x
                    #blocks.get(path[x]).depth = x
                    if x > 0 and path[x].critical is None:
                        path[x].critical = path[x-1]
    return blocks