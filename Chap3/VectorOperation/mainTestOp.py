from VectorOperation import *


# vec = [1,2,3]
# vec2 = [1,2,3]
# print(Magnitude(vec,3))

# print(Negation(vec,3))
# print(Negation(vec,3))

# print(Normalize(vec,3))

# print(ScalarMultiplication(vec,3, 2))

# print(Addition(vec,3,vec2,3))


# vec3 = [0,1]
# vec4 = [0,0.5]

# print(DotProduct(vec3,2,vec4, 2))


# print(CrossProduct(vec3,3,vec4, 3))



matrix = [
     [1,2,3,4],
     [1,2,3,4],
     [1,2,3,4],
     [1,2,3,4]
     ]

# matrix2 = [
#     [1,2,3,4],
#     [1,2,3,4],
#     [1,2,3,4],
#     [1,2,3,4]
#     ]

vec = [1,2,3,4]
# # print(ScalarMulMatrix(matrix, 2))

# print(MatrixMultiplication(matrix,matrix2))

print(MatrixVectorMul(matrix, vec , 4))


# vecCart = [1,2,3]

# print(CartToHom(vecCart, 3))

# vecHom = [1,2,3,4]
# print(HomToCart(vecHom, 4))