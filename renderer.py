import math
import numpy as np


class Renderer:
    def __init__(self, screen, camera, meshes, light):
        self.screen = screen
        self.camera = camera
        self.meshes = meshes
        self.light = light

    
    def render(self, shading, bg_color, ambient_light):
        # Store Depth from Normalized Device Coordinates
        z_buffer = np.full((self.screen.height, self.screen.width), -np.inf)
        # Create image buffer filled with background color
        image_buffer = np.full((self.screen.height, self.screen.width, 3), bg_color) 
        for mesh in self.meshes:
            for face, normal in zip(mesh.faces, mesh.normals):
                # Get world coordinates of face vertices
                world_verts = [mesh.transform.apply_to_point(mesh.verts[i]) for i in face]

                # Project vertices to screen space
                camera_verts = [self.camera.project_point(v) for v in world_verts]
                # device to screen coordinate transformation
                screen_verts = [self.screen.device_to_screen(v) for v in camera_verts]


                # Calculate bounding box
                min_x = max(0, int(min(v[0] for v in screen_verts)))
                max_x = min(self.screen.width, int(max(v[0] for v in screen_verts)))
                min_y = max(0, int(min(v[1] for v in screen_verts)))
                max_y = min(self.screen.height, int(max(v[1] for v in screen_verts)))
    
                for y in range(min_y, max_y):
                    for x in range(min_x, max_x):
                        
                        # Compute Barycentric Coordinates
                        x_a, y_a = screen_verts[0][0], screen_verts[0][1]
                        x_b, y_b = screen_verts[1][0], screen_verts[1][1] 
                        x_c, y_c = screen_verts[2][0], screen_verts[2][1]

                        delL = (y_a - y_b)*x_c + (x_b - x_a)*y_c + (x_a * y_b) - (x_b * y_a)
                        delB = (y_a - y_c)*x_b + (x_c - x_a)*y_b + (x_a * y_c) - (x_c * y_a)

                        if delL == 0.0 or delB == 0.0:
                            lam = -1
                            beta = -1
                            alpha = -1
                        else: 
                            lam = ((y_a - y_b)* x + (x_b - x_a)*y + (x_a * y_b) - (x_b * y_a)) / delL
                            beta = ((y_a - y_c)* x + (x_c - x_a)*y + (x_a * y_c) - (x_c * y_a)) / delB
                            alpha = 1 - beta - lam

                        # Check if the pixel in the triangle
                        if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= lam <= 1:
                            current_depth = alpha * screen_verts[0][2] + beta * screen_verts[1][2] + lam * screen_verts[2][2]

                            if current_depth > z_buffer[x, y]:
                                # Update the Z-buffer with the new depth
                                z_buffer[x, y] = current_depth
                                shader = None
                                if shading == "barycentric":
                                    shader = (
                                        int(alpha * 255),
                                        int(beta * 255),
                                        int(lam * 255)
                                    )
                                elif shading == "flat":
                                    P_world = (world_verts[0] + world_verts[1] + world_verts[2]) / 3

                                    # Get normal vector and it direction
                                    normal = normal / np.linalg.norm(normal) 
                                    normal_dir = mesh.transform.apply_to_normal(normal)

                                    # Calculate light direction
                                    light_pos = np.array(self.light.transform.get_position())
                                    light_dis = light_pos - P_world
                                    light_dir =  light_dis/ np.linalg.norm(light_dis)

                                    # Dot product between normal and light direction
                                    dot_prod =  max(0, np.dot(normal_dir, light_dir))

                                    # Calculate diffuse light
                                    I_d = (self.light.color * self.light.intensity) / (np.linalg.norm(light_dis)**2)
                                    phi_d = (mesh.kd * dot_prod * mesh.diffuse_color) / (math.pi)
                                    D = (I_d * phi_d)

                                    # Calculate ambient light
                                    A = [c * mesh.ka  for c in ambient_light]

                                    shader = (A + D) * 255

                                elif shading == "phong-blinn":
                                    
                                    # Get normal vector and it direction
                                    P_world = (alpha * world_verts[0] + beta* world_verts[1] + lam * world_verts[2])
                                    vertex_normal = [(mesh.vertex_normals[i]/ np.linalg.norm(mesh.vertex_normals[i])) for i in face]
                                    interpolate_coord = (alpha * vertex_normal[0] + beta * vertex_normal[1] + lam * vertex_normal[2])
                                    interpolate_normal_vect = interpolate_coord / np.linalg.norm(interpolate_coord)
                                    interpolate_normal_dir = mesh.transform.apply_to_normal(interpolate_normal_vect)

                                    # Get camera space
                                    camera_space = self.camera.transform.get_position()
                                    
                                    
                                    # Calculate light direction
                                    light_pos = self.light.transform.get_position()
                                    light_dis = light_pos - P_world
                                    light_dir =  light_dis/ np.linalg.norm(light_dis)

                                    # Dot product between normal and light direction
                                    dot_nl =  max(0, np.dot(interpolate_normal_dir, light_dir))

                                    # Calculate diffuse light
                                    I_d = (self.light.color * self.light.intensity) / (np.linalg.norm(light_dis)**2)
                                    phi_d = (mesh.kd * dot_nl * mesh.diffuse_color) / (math.pi)
                                    D = (I_d * phi_d)

                                    # Dot product between H and N
                                    view_dir = (camera_space - P_world) / np.linalg.norm(camera_space - P_world) 
                                    half_vector = (light_dir + view_dir) / np.linalg.norm(light_dir + view_dir)
                                    dot_hn =  max(0, np.dot(interpolate_normal_dir, half_vector ))

                                    # Calculate specular light
                                    I_s = mesh.specular_color
                                    phi_s = mesh.ks * (dot_hn ** mesh.ke)
                                    S = (I_s * phi_s)

                                    # Calculate ambient light
                                    A = [c * mesh.ka  for c in ambient_light]

                                    shader = (A + D + S) * 255

                                image_buffer[x, y] = shader
        self.screen.draw(image_buffer)


          

    