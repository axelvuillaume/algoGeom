import sys
from const import *
from TriangleMesh import TriangleMesh
from VectorOperation.VectorOperation import *
from Scene import *
import pygame
clock = pygame.time.Clock()
from DebugRenderer import DebugRenderer
from RotationRender import *


pygame.init()

# # Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('oui')
running = True

vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

faces = [
    [0, 1, 2], [2, 3, 0], # Face avant
    [4, 5, 6], [6, 7, 4], # Face arrière
    [0, 1, 5], [5, 4, 0], # Face inférieure
    [2, 3, 7], [7, 6, 2], # Face supérieure
    [0, 3, 7], [7, 4, 0], # Face gauche
    [1, 2, 6], [6, 5, 1]  # Face droite
]








def apply_transformations(mesh, model_matrix, projection_matrix, viewport_matrix):
    transformed_vertices = mesh.transform(model_matrix)
    projected_vertices = []
    
    for v in transformed_vertices:
        v_homogeneous = CartToHom(v,3)
        v_projected = MatrixVectorMul(projection_matrix,v_homogeneous,4)
        v_projected = MatrixVectorMul(viewport_matrix,v_projected,4)
        projected_vertices.append(v_projected[:3])
    return projected_vertices


def render_wireframe(screen, mesh, model_matrix, projection_matrix, viewport_matrix):

    screen.fill(BLACK)
    projected_vertices = apply_transformations(mesh, model_matrix, projection_matrix, viewport_matrix)
        
        
    for face in mesh.faces:
        v0 = projected_vertices[face[0]]
        v1 = projected_vertices[face[1]]
        v2 = projected_vertices[face[2]]
        pygame.draw.line(screen, WHITE, (v0[0], v0[1]), (v1[0], v1[1]), 1)
        pygame.draw.line(screen,WHITE, (v1[0], v1[1]), (v2[0], v2[1]), 1)
        pygame.draw.line(screen, WHITE, (v2[0], v2[1]), (v0[0], v0[1]), 1)
        
    
    
    debugRenderer.displayMatrix(rotation_matrix, 50, 50, "Matrice de Rotation")
    debugRenderer.displayMatrix(model_matrix, 50, 200, "Matrice de Modèle")
    debugRenderer.displayVector(euler, 50, 350, "Euler")
    debugRenderer.displayEuler(exponentielMap[0],exponentielMap[1], 50, 500,"Exponentiel map")
    debugRenderer.displayVector(rotation ,400,50, "rotation")
    debugRenderer.displayVector(target_angles ,400,150, "target rotation")
    debugRenderer.displayVector(quaternions, 600, 200, "quaternions")


    

    pygame.display.flip()
   
# transformedVertices = cubeMesh.transform(modelMatrix(2))
# print(transformedVertices)

font = pygame.font.Font(None, 15)
debugRenderer = DebugRenderer(screen, font)
scale= 1
rotation = [0,0,0]
translation = [0,0,0]
animation_active = False  

rotation_speed = 0.005
target_angles = [0, 0, 0]


target_matrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
t = 0
animation_duration = 2
threshold = 0.01
animation_active_Exp = False




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        animation_active = True
    if keys[pygame.K_p]:
        animation_active_Exp = True
    if keys[pygame.K_UP]:
        scale += 0.0001
    if keys[pygame.K_DOWN]:
        scale -= 0.0001
    if keys[pygame.K_q]:
        translation[0] -= 0.001
    if keys[pygame.K_d]:
        translation[0] += 0.001
    if keys[pygame.K_z]:
        translation[1] += 0.001
    if keys[pygame.K_s]:
        translation[1] -= 0.001
    if keys[pygame.K_m]:
        translation[2] += 0.005
    if keys[pygame.K_n]:
        translation[2] -= 0.005
    if keys[pygame.K_KP0]:
        rotation[0] += 0.001
    if keys[pygame.K_KP1]:
        rotation[0] -= 0.001
    if keys[pygame.K_KP2]:
        rotation[1] += 0.001
    if keys[pygame.K_KP3]:
        rotation[1] -= 0.001
    if keys[pygame.K_KP4]:
        rotation[2] += 0.001
    if keys[pygame.K_KP5]:
        rotation[2] -= 0.001
        

    if animation_active : 
        rotation = lerp_euler(rotation, target_angles, rotation_speed)
        if all(math.isclose(r, 0, abs_tol=0.001) for r in rotation):
            rotation = [0, 0, 0] 
            animation_active = False
        

    cubeMesh = TriangleMesh(vertices, faces)
    cubeMesh.modelMatrix(scale, rotation, translation)
    rotation_matrix = cubeMesh.rotationMatrix
    model_matrix = cubeMesh.modelMatrixRes
    
    projection_matrix = Scene.projectionMatrix(-6, 6, -8, 8, -1, 1)
    viewport_matrix = Scene.viewportMatrix(0, 0, 800, 600,)
    

    # Orientation
    euler = MatrixToEuler(rotation_matrix)
    exponentielMap = getExponentialMap(rotation_matrix)
    quaternions = ExpMapToQuaternion(exponentielMap[1],exponentielMap[0])
    
    #LERP
    eulerMatrix = eulerToMatrix(euler[0],euler[1],euler[2])
    TestMatric = ExpMapToMatrix(exponentielMap[0], exponentielMap[1])
    
    render_wireframe(screen, cubeMesh, model_matrix, projection_matrix, viewport_matrix)
    

    clock.tick(3000)

pygame.quit()