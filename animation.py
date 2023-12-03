import numpy as np
import math
from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight


class Animation:
    def __init__(self):
        # Initialize animation properties
        pass

def main():
    # Create instances of the classes and set up the animation pipeline
    pass

if __name__ == "__main__":
    screen = Screen(500,500)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 5, 0)


    mesh = Mesh.from_stl("teapot.stl", np.array([1.0, 0.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.05,1.0,0.5,1000)
    mesh.transform.set_rotation(0, 0, 75)
    
    mesh.sphere_uvs()
    mesh.load_texture("earth.jpg")

    light = PointLight(50.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [mesh], light)
    renderer.render("texture-correct",[80,80,80], [0.2, 0.2, 0.2])

    screen.show()
