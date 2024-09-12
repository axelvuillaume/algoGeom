import math
from VectorOperation.VectorOperation import *

def MatrixToEuler(matrix):
    
    singular = math.sqrt(matrix[0][0]**2 + matrix[1][0]**2)

    if singular > 1e-6 : 
        alpha = math.atan2(matrix[2][1], matrix[2][2])  
        beta = math.atan2(-matrix[2][0], singular)     
        gamma = math.atan2(matrix[1][0], matrix[0][0]) 
    else:
        alpha = 0
        if matrix[2][0] < 0:
            beta = math.pi / 2  
        else:
            beta = -math.pi / 2 
        gamma = math.atan2(-matrix[0][1], matrix[0][2])

    return alpha, beta, gamma


def getExponentialMap(matrix):
        m = matrix
        angle = math.acos((m[0][0] + m[1][1] + m[2][2] - 1) / 2)
        
        if angle > 1e-6:
            x = (m[2][1] - m[1][2]) / (2 * math.sin(angle))
            y = (m[0][2] - m[2][0]) / (2 * math.sin(angle))
            z = (m[1][0] - m[0][1]) / (2 * math.sin(angle))
        else:
            x, y, z = 0, 0, 0
        
        return angle, [x, y, z]


    
def eulerToMatrix(alpha, beta, gamma):
    # Matrices de rotation autour des axes X, Y et Z
    Rx = [
        [1, 0, 0, 0],
        [0, math.cos(alpha), -math.sin(alpha), 0],
        [0, math.sin(alpha), math.cos(alpha), 0],
        [0, 0, 0, 1]
    ]
    
    Ry = [
        [math.cos(beta), 0, math.sin(beta), 0],
        [0, 1, 0, 0],
        [-math.sin(beta), 0, math.cos(beta), 0],
        [0, 0, 0, 1]
    ]
    
    Rz = [
        [math.cos(gamma), -math.sin(gamma), 0, 0],
        [math.sin(gamma), math.cos(gamma), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]
    
    matrice = MatrixMultiplication(Rz,MatrixMultiplication(Ry, Rx))
    
    return matrice

def lerp(a, b, t):
    return a + t * (b - a)


def lerp_euler(current_angles, target_angles, t):
    return [
        lerp(current_angles[0], target_angles[0], t),  # X-axis
        lerp(current_angles[1], target_angles[1], t),  # Y-axis
        lerp(current_angles[2], target_angles[2], t)   # Z-axis
    ]
    


def ExpMapToMatrix(angle,axis):
    axis = Normalize(axis,3) 
    x, y, z = axis
    c = math.cos(angle)
    s = math.sin(angle)
    t = 1 - c

    matrice = [
        [t*x*x + c,     t*x*y - s*z,   t*x*z + s*y, 0],
        [t*x*y + s*z,   t*y*y + c,     t*y*z - s*x, 0],
        [t*x*z - s*y,   t*y*z + s*x,   t*z*z + c, 0],
        [0,0,0,1]
    ]
        
    return matrice

def ExpMapToQuaternion(axis, angle):
    axis = Normalize(axis,3)
    s = math.sin(angle / 2.0)
    c = math.cos(angle / 2.0)
    
    qua = [
        axis[0] * s,
        axis[1] * s,
        axis[2] * s,
        c
    ]
    
    return qua


def quaternion_to_matrix(q):
    w, x, y, z = q
    matrix = [
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w, 0],
        [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w, 0],
        [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2, 0],
        [0, 0, 0, 1]
    ]
    
    return matrix

def lerp_quaternions(q1, q2, t):
    q1 = np.array(q1)
    q2 = np.array(q2)
    dot_product = np.dot(q1, q2)
    if dot_product < 0.0:
        q2 = -q2
        dot_product = -dot_product
    if dot_product > 0.95:
        q = q1 + t * (q2 - q1)
        q = q / np.linalg.norm(q)
    else:
        theta_0 = math.acos(dot_product)
        theta = theta_0 * t
        q2 = q2 - q1 * dot_product
        q2 = q2 / np.linalg.norm(q2)
        q = q1 * math.cos(theta) + q2 * math.sin(theta)
    
    return q
