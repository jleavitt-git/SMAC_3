'''
Disclaimer: This solution is not scalable for creating a big world.
Creating a game like Minecraft requires specialized knowledge and is not as easy
to make as it looks.
You'll have to do some sort of chunking of the world and generate a combined mesh
instead of separate blocks if you want it to run fast. You can use the Mesh class for this.
You can then use blocks with colliders like in this example in a small area
around the player so you can interact with the world.
'''

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from block import Block
import filesupport as fs

app = Ursina()

blocks = []
# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.
def printBlocks(blocks):
    for b in blocks:
        print("ID: ", b.id, " X: ", b.xs, " Y: ", b.ys, " Z: ", b.zs)

def delBlock(x, y, z):
    for b in blocks:
        if b.xs == x and b.ys == y and b.zs == z:
            blocks.remove(b)

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color = color.lime,
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                voxel = PlayerVoxel(position=self.position + mouse.normal)
                vector = self.position + mouse.normal
                blocks.append(Block(str(random.randrange(0,10000)), vector.x, vector.y, vector.z))

class backgroundVoxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.rgb(40, 40, 40),
            highlight_color = color.black,
        )

class PlayerVoxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 100, random.uniform(.9, 1.0)),
            highlight_color = color.rgb(242, 59, 144),
        )
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                vector = self.position + mouse.normal
                voxel = PlayerVoxel(position=vector)
                blocks.append(Block(str(random.randrange(0,10000)), vector.x, vector.y, vector.z))

            if key == 'right mouse down':
                vector = self.position
                delBlock(vector.x, vector.y, vector.z)
                destroy(self)

for z in range(-10,20):
    for x in range(-10,20):
        if not (x >= 0 and x < 10 and z >= 0 and z < 10):
            voxel = backgroundVoxel(position=(x,-1,z))

for z in range(10):
    for x in range(10):
        voxel = Voxel(position=(x,-1,z))

def input(key):
    if key == 'escape':
        fs.printToFile(blocks, 'struct.txt')
        quit()

# def input(key):
#     if key == 'left mouse down':
#         hit_info = raycast(camera.world_position, camera.forward, distance=5)
#         if hit_info.hit:
#             Voxel(position=hit_info.entity.position + hit_info.normal)


def main():
    player = FirstPersonController()
    app.run()

if __name__ == "__main__":
    main()