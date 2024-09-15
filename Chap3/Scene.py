import math
from VectorOperation.VectorOperation import *

class Scene:
    
    def projectionMatrixPersp(theta,n,f,a):
        
        d = 1/math.tan(theta/2)
        return [
            [d/a,0,0,0],
            [0,d,0,0],
            [0,0,(n+f)/(n-f),(2*n*f)/(n-f)],
            [0,0,-1,0],
        ]
    
    def viewMatrix(v1, v2, v3, camera_position):
        rotation_matrix = [
            [v1[0], v2[0], v3[0], 0],
            [v1[1], v2[1], v3[1], 0],
            [v1[2], v2[2], v3[2], 0],
            [0, 0, 0, 1]
        ]
        
        translation_matrix = [
            [1, 0, 0, camera_position[0]],
            [0, 1, 0, -camera_position[1]],
            [0, 0, 1, camera_position[2]],
            [0, 0, 0, 1]
        ]
        
        return MatrixMultiplication(rotation_matrix, translation_matrix)
        
    def viewportMatrix(sx, sy, hs, ws, ns, fs):
        return [
            [ws/2, 0, 0 ,sx + ws/2],
            [0, hs/2, 0 , sy+hs/2],
            [0,0,(fs-ns)/2, (ns+fs)/2],
            [0,0,0,1],
        ]
        
    def projectionMatrixOrtho(l,r,t,b,n,f):
        return [
            [2/(r-l), 0, 0 ,-((r+l)/(r-l))],
            [0, 2/(t-b), 0 , -((t+b)/(t-b))],
            [0,0,(-2)/(f-n), -((f+n)/(f-n))],
            [0,0,0,1],
        ]
        
