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
        
        return [angle, [x, y, z]]


    
def eulerToMatrix(alpha, beta, gamma):
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
        c,
        axis[0] * s,
        axis[1] * s,
        axis[2] * s,
        
    ]
    
    return qua


def QuatToMatrix(q):
    w, x, y, z = q
    matrix = [
        [1 - 2*y**2 - 2*z**2, 2*x*y - 2*z*w, 2*x*z + 2*y*w, 0],
        [2*x*y + 2*z*w, 1 - 2*x**2 - 2*z**2, 2*y*z - 2*x*w, 0],
        [2*x*z - 2*y*w, 2*y*z + 2*x*w, 1 - 2*x**2 - 2*y**2, 0],
        [0, 0, 0, 1]
    ]
    
    return matrix



def NormalizeQuat(quat):
    length = math.sqrt(quat[0]**2 + quat[1]**2 + quat[2]**2 + quat[3]**2)
    return [quat[0] / length, quat[1] / length, quat[2] / length, quat[3] / length]

def QuatProduct(q1, q2):
    return q1[0] * q2[0] + q1[1] * q2[1] + q1[2] * q2[2] + q1[3] * q2[3]


def SlerpQuat(q1, q2, t):
    
    product = QuatProduct(q1, q2)
    
    if product < 0.0:
        q2 = Negation(q2,4)
        product = -product
        
    if product > 0.995:
        result = [
            q1[0] + t * (q2[0] - q1[0]),
            q1[1] + t * (q2[1] - q1[1]),
            q1[2] + t * (q2[2] - q1[2]),
            q1[3] + t * (q2[3] - q1[3])
        ]
        return NormalizeQuat(result)
    
    else:
        theta = math.acos(product)
        
        s1 = math.sin((1 - t) * theta) / math.sin(theta)
        s2 = math.sin(t * theta) / math.sin(theta)
        
        result = [
            s1 * q1[0] + s2 * q2[0],
            s1 * q1[1] + s2 * q2[1],
            s1 * q1[2] + s2 * q2[2],
            s1 * q1[3] + s2 * q2[3]
        ]
        
        return result


def QuaternionToAcardanAngles(q):

    w, x, y, z = q
    
    theta_x = math.atan2(2 * (w * x + y * z), 1 - 2 * (x**2 + y**2))
    theta_y = math.asin(2 * (w * y - z * x))
    theta_z = math.atan2(2 * (w * z + x * y), 1 - 2 * (y**2 + z**2))
    
    return [theta_x, theta_y, theta_z]


def matrixToAcardanAngles(rotation_matrix):
    r00 = rotation_matrix[0][0]
    r01 = rotation_matrix[0][1]
    r02 = rotation_matrix[0][2]
    r10 = rotation_matrix[1][0]
    r11 = rotation_matrix[1][1]
    r12 = rotation_matrix[1][2]
    r20 = rotation_matrix[2][0]
    r21 = rotation_matrix[2][1]
    r22 = rotation_matrix[2][2]

    # Calcul des angles d'Acardan (en radians)
    if r20 < 1:
        if r20 > -1:
            # Cas général
            theta_y = math.asin(-r20)
            theta_x = math.atan2(r21, r22)
            theta_z = math.atan2(r10, r00)
        else:
            # Gimbal lock : theta_y = -pi/2
            theta_y = math.pi / 2
            theta_x = -math.atan2(-r01, r11)
            theta_z = 0
    else:
        # Gimbal lock : theta_y = pi/2
        theta_y = -math.pi / 2
        theta_x = math.atan2(-r01, r11)
        theta_z = 0

    # Retourne les angles d'Acardan (ou les angles XYZ)
    return [theta_x, theta_y, theta_z]
