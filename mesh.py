import numpy as np
from stl import mesh
from transform import Transform

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

    
class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
