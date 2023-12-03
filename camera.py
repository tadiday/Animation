from transform import Transform
import numpy as np
from mesh import Mesh

class OrthoCamera:
    def __init__(self, left,  right,  bottom, top,  near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.transform = Transform()

    def ratio(self):
        width = self.left - self.right
        height = self.top - self.bottom
        return width/height
    
    def project_point(self, p):
        space = self.transform.apply_inverse_to_point(p)
        space = np.append(space, 1)
        projection_matrix = np.array([
            [-2 / (self.right - self.left), 0, 0, - (self.right + self.left) / (self.right - self.left)],
            [0, 0, 2 / (self.top - self.bottom), - (self.top + self.bottom) / (self.top - self.bottom)],
            [0, 2 / (self.near - self.far), 0, - (self.near + self.far) / (self.near - self.far)],
            [0, 0, 0, 1]
         ])
        projected_point = np.array(np.dot(projection_matrix, space))
        return projected_point[:3]

    def inverse_project_point(self, p):
        # Step 1: Create the perspective projection matrix
        projection_matrix = np.array([
            [2 / (self.right - self.left), 0, 0, - (self.right + self.left) / (self.right - self.left)],
            [0, 0, 2 / (self.top - self.bottom), - (self.top + self.bottom) / (self.top - self.bottom)],
            [0, 2 / (self.near - self.far), 0, - (self.near + self.far) / (self.near - self.far)],
            [0, 0, 0, 1]
         ])

        # Perform inverse orthographic projection
        p_unprojected = np.matmul(np.linalg.inv(projection_matrix), np.append(p, 1))

        # Transform point back to world coordinates

        return self.transform.apply_to_point(p_unprojected[:3])
    
class PerspectiveCamera:
    def __init__(self, left,  right,  bottom, top,  near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.transform = Transform()

    def ratio(self):
        width = self.left - self.right
        height = self.top - self.bottom
        return width/height

    def project_point(self, p):
        space = self.transform.apply_inverse_to_point(p)
        space = np.append(space, 1)
        projection_matrix = np.array([
            [-self.near, 0, 0, 0],
            [0, self.near + self.far, 0, -self.near * self.far],
            [0, 0, self.near, 0],
            [0, 1, 0, 0]
        ])
        apply_P = np.dot(projection_matrix, space)
        ortho_matrix = np.array([
            [2 / (self.right - self.left), 0, 0, - (self.right + self.left) / (self.right - self.left)],
            [0, 2 / (self.near - self.far), 0, - (self.near + self.far) / (self.near - self.far)],
            [0, 0, 2 / (self.top - self.bottom), - (self.top + self.bottom) / (self.top - self.bottom)],
            [0, 0, 0, 1]
         ])
        apply_P /= apply_P[3]
        apply_O = np.dot(ortho_matrix, apply_P)
        temp = apply_O[1]
        apply_O[1] = apply_O[2]
        apply_O[2] = temp
        return apply_O[:3]


    def inverse_project_point(self, p):
        temp = p[1]
        p[1] = p[2]
        p[2] = temp

        ortho_matrix = np.array([
            [2 / (self.right - self.left), 0, 0, - (self.right + self.left) / (self.right - self.left)],
            [0, 2 / (self.near - self.far), 0, - (self.near + self.far) / (self.near - self.far)],
            [0, 0, 2 / (self.top - self.bottom), - (self.top + self.bottom) / (self.top - self.bottom)],
            [0, 0, 0, 1]
         ])
        apply_O_inv = np.matmul(np.linalg.inv(ortho_matrix), np.append(p, 1))
        y =  (self.near * self.far) /((self.near + self.far) -  apply_O_inv[1])
        apply_O_inv *= y

        projection_matrix = np.array([
            [self.near, 0, 0, 0],
            [0, self.near + self.far, 0, -self.near * self.far],
            [0, 0, self.near, 0],
            [0, 1, 0, 0]
        ])
        apply_P_inv = np.dot(np.linalg.inv(projection_matrix), apply_O_inv)
        return self.transform.apply_to_point(apply_P_inv[:3])
    
    def inverse_project_w(self, p):
        temp = p[1]
        p[1] = p[2]
        p[2] = temp

        ortho_matrix = np.array([
            [2 / (self.right - self.left), 0, 0, - (self.right + self.left) / (self.right - self.left)],
            [0, 2 / (self.near - self.far), 0, - (self.near + self.far) / (self.near - self.far)],
            [0, 0, 2 / (self.top - self.bottom), - (self.top + self.bottom) / (self.top - self.bottom)],
            [0, 0, 0, 1]
         ])
        apply_O_inv = np.matmul(np.linalg.inv(ortho_matrix), np.append(p, 1))
        y =  (self.near * self.far) /((self.near + self.far) -  apply_O_inv[1])
        return y
