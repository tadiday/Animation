import numpy as np
import math

import pygame

from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight
from scipy.spatial.transform import Rotation as R
from scipy.spatial.transform import Slerp

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


    mesh = Mesh.from_stl("teapot.stl", np.array([0.5, 0.5, 0.5]),\
        np.array([1.0, 1.0, 1.0]),0.05,1.0,0.5,1000)
    mesh2 = Mesh.from_stl("uploads_files_2370210_StoneCup.stl", np.array([1, 1, 1]),\
        np.array([1.0, 1.0, 1.0]),0.05,1.0,0.5,1000)
    mesh2.transform.set_position(4,0,0)
    mesh2.transform.set_rotation(0,0,15)
    num_frames = 65
    mesh.load_texture("ocean-seawater-wind-wave-ocean.jpg")
    mesh2.load_texture("ocean-seawater-wind-wave-ocean.jpg")
    z_rotation_quaternion = None
    j = 0
    for i in range(num_frames-10):

        angle = (i / num_frames) * 2 * np.pi
        quaternion = R.from_euler('xyz', [0,0 , np.degrees(angle)], degrees=True)

        mesh.transform.set_quaternion_rotation(np.array((quaternion.as_quat())))
        z_rotation_quaternion = quaternion

        light = PointLight(50.0, np.array([1, 1, 1]))
        light.transform.set_position(0, 5, 5)

        renderer = Renderer(screen, camera, [mesh], light)
        renderer.render("phong-blinn",[80,80,80], [0.2, 0.2, 0.2],filename=f"frame_{j}.png")
        j = j+1
    for i in range(8):
        # Get the current position

        current_position = mesh.transform.get_position()
        mesh.transform.set_position(current_position[0], current_position[1], current_position[2] + 0.2)
        angle = (i / num_frames) * (1/4) * np.pi
        quaternion = R.from_euler('xyz', [0, np.degrees(angle), 0], degrees=True) * z_rotation_quaternion
        z_rotation_quaternion = quaternion
        mesh.transform.set_quaternion_rotation(np.array((quaternion.as_quat())))
        # Set the new position using the set_position method

        light = PointLight(50.0, np.array([1, 1, 1]))
        light.transform.set_position(0, 5, 5)
        mesh2_curr_pos = mesh2.transform.get_position()
        mesh2.transform.set_position(mesh2_curr_pos[0]-0.2,mesh2_curr_pos[1],mesh2_curr_pos[2])
        renderer = Renderer(screen, camera, [mesh,mesh2], light)
        renderer.render("phong-blinn", [80, 80, 80], [0.2, 0.2, 0.2], filename=f"frame_{j}.png")
        j = j + 1
    for i in range(4):
        angle = (i / num_frames) * (1/2) * np.pi
        quaternion = R.from_euler('xyz', [0, np.degrees(angle), 0], degrees=True) * z_rotation_quaternion

        mesh.transform.set_quaternion_rotation(np.array((quaternion.as_quat())))

        light = PointLight(50.0, np.array([1, 1, 1]))
        light.transform.set_position(0, 5, 5)
        # mesh2_curr_pos = mesh2.transform.get_position()
        # mesh2.transform.set_position(mesh2_curr_pos[0] - 0.2, mesh2_curr_pos[1], mesh2_curr_pos[2])
        renderer = Renderer(screen, camera, [mesh,mesh2], light)
        renderer.render("phong-blinn", [80, 80, 80], [0.2, 0.2, 0.2], filename=f"frame_{j}.png")
        j = j + 1
    #     #screen.show()