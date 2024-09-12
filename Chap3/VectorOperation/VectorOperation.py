import math

def Magnitude(vector, size):
    res = 0
    for i in range(size):
        res += vector[i]*vector[i]
        
    resFinal = math.sqrt(res)
    return resFinal

def Negation(vector, size):
    for i in range(size):
        vector[i] = -vector[i]
    return vector

def Normalize(vector, size):
    res = []
    if Magnitude(vector, size) == 0:
        return [0]*size
    else :
        for i in range(size):
            res.append(vector[i]/ Magnitude(vector, size))
        return res


def ScalarMultiplication(vector, size, scalar):
    for i in range(size):
        vector[i] = vector[i] * scalar
    return vector

def Addition(vector1, size1, vector2, size2):
    if size1 == size2:
        vectorRes = []
        for i in range(size1):
            vectorRes.append(vector1[i] + vector2[i])
    
        return vectorRes
    
    else:
        raise ValueError("Pas meme taille")


    

def Subtraction(vector1, size1, vector2,size2):
    if size1 == size2:
        vectorRes = []
        for i in range(size1):
            vectorRes.append(vector1[i] - vector2[i])
        return vectorRes
    
    else:
        raise ValueError("Pas meme taille")
        
def DotProduct(vector1, size1, vector2,size2):
    if size1 == size2:
        vectorRes = 0
        for i in range(size1):
            vectorRes += vector1[i] * vector2[i]
        
        if vectorRes == 0 :
            print("perpendicular")
            return vectorRes
        
        elif vectorRes < 0 :
            print("opposite direction")
            return vectorRes
        
        elif vectorRes > 0 :
            print("same direction")
            return vectorRes
        
    else:
        raise ValueError("Pas meme taille")
    
    
def CrossProduct(vector1, size1, vector2, size2):
    if size1 == size2 & size1 == 3 :
        vectorRes = [
            vector1[1] * vector2[2] - vector1[2] * vector2[1],  # x
            vector1[2] * vector2[0] - vector1[0] * vector2[2],  # y
            vector1[0] * vector2[1] - vector1[1] * vector2[0]   # z
        ]
        
        return vectorRes
    
    else:
        raise ValueError("Pas meme taille")
            

def ScalarMulMatrix(matrix ,scalar) :
    # on travaille que sur de matrice 4 ligne
    for i in range(4):
        for j in range(4):
            matrix[i][j] = scalar* matrix[i][j]
        
    return matrix


def MatrixMultiplication( matrix1, matrix2):
    MatrixRes = [[0] * 4 for _ in range(4)]
    
    res = 0
    for row in range(4):
        for col in range(4):
            res = 0
            for k in range(4):
                res += matrix1[row][k] * matrix2[k][col]
            MatrixRes[row][col] = res
       
    
    return MatrixRes
    
def MatrixVectorMul ( matrix, vector,size):
    vectorRes = []
    if size == 4 :
        col = 0
        res = 0
        for row in range(4):
            for col in range(4):
                res += vector[col] * matrix[row][col]
            
            vectorRes.append(res)
            res = 0
        return vectorRes
    
    else :
        raise ValueError (" size pas egale a 4 ")

def CartToHom (vector, size):
    if size == 3:
        vector.append(1)
        return vector
    else:
        raise ValueError (" taille doit etre egal a 3")

def HomToCart (vector, size):
    vectorRes = []
    if size == 4:
        if vector[3] != 0:
            for i in range(size-1):
                vectorRes.append(vector[i] / vector[3])
            
            return vectorRes
        else:
            raise ValueError ("vector[3] == 0")
    else:
        raise ValueError (" size != 4")
    
def Inverse(matrix):
        return "aled"
    
    
def Determinant(matrix):
    return "ouioui"