import numpy as np
import math
from scipy.spatial.transform import Rotation

class Transform:
    def __init__(self):
        self.matrix = np.identity(4)
        self.rotation = Rotation.identity()

    def get_position(self):
        return self.matrix[0, 3], self.matrix[1, 3], self.matrix[2, 3]

    def transformation_matrix(self):
        return self.matrix

    def set_position(self, x, y, z):
        self.matrix[0, 3] = x
        self.matrix[1, 3] = y
        self.matrix[2, 3] = z

    def set_rotation(self, x, y ,z):
        # X rotation
        tempX = np.identity(4)
        tempX[1, 1] = math.cos(math.radians(x))
        tempX[1, 2] = -math.sin(math.radians(x))
        tempX[2, 1] = math.sin(math.radians(x))
        tempX[2, 2] = math.cos(math.radians(x))
        self.matrix = np.matmul(self.matrix, tempX)


        # Y rotation
        tempY = np.identity(4)

        tempY[0, 0] = math.cos(math.radians(y))
        tempY[0, 2] = math.sin(math.radians(y))
        tempY[2, 0] = -math.sin(math.radians(y))
        tempY[2, 2] = math.cos(math.radians(y))
        self.matrix = np.matmul(self.matrix, tempY)

        # Z rotation
        tempZ = np.identity(4)

        tempZ[0, 0] = math.cos(math.radians(z))
        tempZ[0, 1] = -math.sin(math.radians(z))
        tempZ[1, 0] = math.sin(math.radians(z))
        tempZ[1, 1] = math.cos(math.radians(z))
        self.matrix = np.matmul(self.matrix, tempZ)

    def set_quaternion_rotation(self, quaternion):
        self.rotation = Rotation.from_quat(quaternion)
        self.matrix[:3, :3] = self.rotation.as_matrix()

    def inverse_matrix(self):
        return np.linalg.inv(self.matrix)

    def apply_to_point(self, p):
        point = np.append(p, 1)
        result = np.matmul(self.matrix, point)
        return result[:3]

    def apply_inverse_to_point(self, p):
        point = np.append(p, 1)
        inverse = np.linalg.inv(self.matrix)
        result = np.matmul(inverse, point)
        return result[:3]

    def apply_to_normal(self, n):
        normal = np.append(n, 0)
        result = np.matmul(self.matrix, normal)
        return result[:3]
