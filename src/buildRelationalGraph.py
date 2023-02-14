import graphviz
import block
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin/'

'''

Creates relational graph with graphviz

Bit of a pain to set up, you may need to change the os.environ path above

'''

def buildGraph(blocks):
    dot = graphviz.Digraph(engine='circo')

    for b in blocks:
        dot.node(str(b.id), str(b.id))
    for b in blocks:
        if b.critical is not None:
            dot.edge(str(b.id), str(b.critical.id), constraint='false')


    dot.render('doctest-output/round-table.gv', view=True)


def main():
    #SampleData
    b1 = block.Block("one",5,0,5)
    b2 = block.Block("two",5,1,5, b1)
    b3 = block.Block("three",5,2,5, b2)
    b4 = block.Block("four",5,3,5, b3)
    b5 = block.Block("five",4,0,5, b4)
    blocks = [b1,b2,b3,b4,b5]
    buildGraph(blocks)

if __name__ == "__main__":
    main()