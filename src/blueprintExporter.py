import block
import edgeGraph as eg


def exportBlocks(blocks, g):
    with open('blueprint.txt', 'w') as f:
        blocks = sorted(blocks, key=lambda x: x.depth, reverse=False)
        
        for b in blocks:
            string = ""
            string+="{"
            string+="["+str(b.xs)+","+str(b.ys)+","+str(b.zs)+"]:"
            string+=str(int(b.orientation))+":"
            string+=str(int(b.rotation))+":"
            neighbors = g.edges(b)
            count = 0
            for p in blocks:
                if p.id == b.id:
                    break
                count+=1
            if count < len(blocks)-1:
                string+="["+str(blocks[count+1].xs)+","+str(blocks[count+1].ys)+","+str(blocks[count+1].zs)+"]"
            string+=":["
            for n in range(len(neighbors)):
                string+="["+str(neighbors[n].xs)+","+str(neighbors[n].ys)+","+str(neighbors[n].zs)+"]"
                if n != len(neighbors)-1:
                    string+=","
            string+="]}\n"
            f.write(string)