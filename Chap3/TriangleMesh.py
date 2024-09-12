from VectorOperation.VectorOperation import *
import numpy as np

class TriangleMesh:
    def __init__(self, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.modelMatrixRes = [[0] * 4 for _ in range(4)]
        self.rotationMatrix = [[0] * 4 for _ in range(4)]
        
        
        
    def transform(self, matrix):
        transformed_vertices = []
        for v in self.vertices:
            vHomogeneous = CartToHom(v,3)
            transformedV = MatrixVectorMul(matrix,vHomogeneous,4)
            transformed_vertices.append(transformedV[:3])
        return transformed_vertices



    def RotationMapAxis(axis, angle):
        axis = Normalize(axis,3) 
        x, y, z = axis
        c = math.cos(angle)
        s = math.sin(angle)
        t = 1 - c

        matrice = [
            [t*x*x + c,     t*x*y - s*z,   t*x*z + s*y],
            [t*x*y + s*z,   t*y*y + c,     t*y*z - s*x],
            [t*x*z - s*y,   t*y*z + s*x,   t*z*z + c]
        ]
            
        return matrice
    
    
    def SetRotationMatrix(self,rotation): 

        rotation_matrix_x = [
            [1, 0, 0, 0],
            [0,math.cos(rotation[0]), -math.sin(rotation[0]), 0],
            [0, math.sin(rotation[0]), math.cos(rotation[0]), 0],
            [0,0, 0, 1]
        ]
        
        
        rotation_matrix_z = [
            [math.cos(rotation[2]), -math.sin(rotation[2]), 0, 0],
            [math.sin(rotation[2]), math.cos(rotation[2]), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
        
        rotation_matrix_y = [
            [math.cos(rotation[1]), 0, math.sin(rotation[1]), 0],
            [0,1, 0, 0],
            [-math.sin(rotation[1]),0, math.cos(rotation[1]), 0],
            [0,0, 0, 1]
        ]
            
        self.rotationMatrix = MatrixMultiplication(MatrixMultiplication(rotation_matrix_y,rotation_matrix_z),rotation_matrix_x)


    def modelMatrix(self,scale, translation):
        
        # rotation_matrix = axisAngleToRotationMatrix(axis,angle)
        # rotation_matrix_4x4 = np.eye(4)
        # rotation_matrix_4x4[:3, :3] = rotation_matrix
            
    
        scale_matrix = [
            [scale, 0, 0, 0],
            [0, scale, 0, 0],
            [0, 0, scale, 0],
            [0, 0, 0, 1]
        ]
        
        

            
        translation_matrix = [
            [1, 0, 0, translation[0]],
            [0, 1, 0, translation[1]],
            [0, 0, 1, translation[2]],
            [0, 0, 0, 1]
        ]

        
        self.modelMatrixRes = MatrixMultiplication(MatrixMultiplication(translation_matrix, self.rotationMatrix), scale_matrix)
        
        # return rotationMatrix,modelMatrix
        
    
    def updateRotationMatrix(self, new_rotation_matrix):
        self.rotationMatrix = new_rotation_matrix
        scale_matrix = self.modelMatrixRes[0:4][0:4]  
        translation_matrix = self.modelMatrixRes[0:4][0:4] 
        self.modelMatrixRes = MatrixMultiplication(MatrixMultiplication(translation_matrix, self.rotationMatrix), scale_matrix)
