import numpy as np
from stl import mesh
from transform import Transform
from PIL import Image


class Mesh:
    def __init__(self, diffuse_color, specular_color, ka, kd, ks, ke):
        self.verts = []
        self.faces = []
        self.normals = []
        self.vertex_normals = []
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.ka = ka
        self.kd = kd 
        self.ks = ks
        self.ke = ke
        self.transform = Transform()
        self.uvs = []  # New member for texture coordinates
        self.texture = None


    @staticmethod
    def from_stl(stl_path, diffuse_color, specular_color, ka, kd, ks, ke):
        result = Mesh(diffuse_color, specular_color, ka, kd, ks, ke)
        stl_data = mesh.Mesh.from_file(stl_path)

        for triangle in stl_data:
            face = []
            for i in range(3):
                vertex = Vertex(triangle[i * 3], triangle[i * 3 + 1], triangle[i * 3 + 2])
                if (vertex.x, vertex.y, vertex.z) not in result.verts:
                    result.verts.append((vertex.x, vertex.y, vertex.z))
                face.append(result.verts.index((vertex.x, vertex.y, vertex.z)))
            result.faces.append(face)

        for i in stl_data.normals:
            result.normals.append(tuple(i.tolist()))
        
        
        for i in range(len(result.verts)):
            sum_of_normals = np.array([0.0,0.0,0.0])
            count = 0.0
            for j, face in enumerate(result.faces): 
                if i in face:
                    normal = np.array(result.normals[j]) / np.linalg.norm(result.normals[j])
                    sum_of_normals += normal
                    count += 1.0
            average_normal = sum_of_normals / count
            result.vertex_normals.append(average_normal)
        return result

    def load_texture(self, img_path):
            self.texture = np.array(Image.open(img_path))

    #z is 'up', theta is azimith angle, phi is elevation
    #used for texture coordinates of sphere, so it only returns theta and phi angle
    def cart2sph(self, v):
        x = v[0]
        y = v[1]
        z = v[2]

        theta = np.arctan2(y,x)
        phi   = np.arctan2(z,np.sqrt(x**2 + y**2))
        return np.array([theta, phi])


    def sphere_uvs(self):
        uvs = []
        verts = self.verts
        #loop over each vertex
        for v in verts:
            #convert cartesian to spherical
            uv = self.cart2sph(v)
            
            #convert theta and phi to u and v by normalizing angles
            uv[0] += np.pi
            uv[1] += np.pi/2.0

            uv[0] /= 2.0*np.pi
            uv[1] /= np.pi

            uvs.append(uv)

        self.uvs = uvs

        return uvs

    @staticmethod
    def textured_quad():
        mesh = Mesh(
            diffuse_color=(1,1,1), 
            specular_color=(1,1,1),
            ka=0.5,
            kd=0.5, 
            ks=0.5,
            ke=0.5
        )
        # mesh.verts = [np.array([0.4, 0.5, -0.5]),
        #     np.array([-0.4, 0.5, -0.4]),
        #     np.array([0.4, -0.5, 0.4]),
        #     np.array([-0.4, -0.9, 0.4])
        #     ]

        mesh.verts = [np.array([0.4, 0.5, -0.5]),
            np.array([-0.4, 0.5, -0.5]),
            np.array([0.5, -0.5, 0.4]),
            np.array([-0.4, -0.55, 0.4])
            ]

        mesh.faces = [[0, 1, 2],[3, 2, 1]]

        #todo: once happy, print the normals and set manually to avoid dependency on vector3 class
        normals = []
        for face in mesh.faces:
            a = np.array(mesh.verts[face[0]])
            b = np.array(mesh.verts[face[1]])
            c = np.array(mesh.verts[face[2]])
            n = np.cross(b - a, c - a)

            normals.append(n / np.linalg.norm(n))

        mesh.normals = normals 

        mesh.uvs = [np.array([0.0,0.0]),np.array([1.0,0.0]),np.array([0.0,1.0]),np.array([1.0,1.0])]

        return mesh
    
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
