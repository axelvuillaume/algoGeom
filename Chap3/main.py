import sys
from const import *
from TriangleMesh import TriangleMesh
from VectorOperation.VectorOperation import *
from Scene import *
import pygame
clock = pygame.time.Clock()
from DebugRenderer import DebugRenderer
from RotationRender import *
from Event import *


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
    [1, 0, 2], [3, 2, 0], # Face avant
    [4, 5, 6], [6, 7, 4], # Face arrière
    [0, 1, 5], [5, 4, 0], # Face inférieure
    [2, 3, 7], [7, 6, 2], # Face supérieure
    [3, 0, 7], [4, 7, 0], # Face gauche
    [1, 2, 6], [6, 5, 1]  # Face droite
]

identity_matrice = [
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,0],
    [0,0,0,1],
    ]


light_direction = [0, 0, -1]

# Default
# faces = [
#     [0, 1, 2], [2, 3, 0], # Face avant
#     [4, 5, 6], [6, 7, 4], # Face arrière
#     [0, 1, 5], [5, 4, 0], # Face inférieure
#     [2, 3, 7], [7, 6, 2], # Face supérieure
#     [0, 3, 7], [7, 4, 0], # Face gauche
#     [1, 2, 6], [6, 5, 1]  # Face droite
# ]



def calculate_normal(v0, v1, v2):
    edge1 = Subtraction(v1, 3, v0,3)
    edge2 = Subtraction(v2,3, v0,3)
    normal = CrossProduct(edge1,3, edge2,3)
    return Normalize(normal,3)



def diffuse_light_intensity(normal, light_direction):
    return max(0, DotProduct(normal,3, light_direction,3))



def apply_lighting_to_color(base_color, intensity):
    return  [min(255, int(c * (intensity*0.8 + 0.2))) for c in base_color]


def apply_transformations(mesh,view_matrix,model_matrix, projection_matrix, viewport_matrix):
    transformed_vertices = mesh.transform(model_matrix)
    projected_vertices = []
    
    for v in transformed_vertices:
        
        v_transformed = MatrixVectorMul(view_matrix,v,4)

        v_projected = MatrixVectorMul(projection_matrix,v_transformed,4)
 
        v_result = MatrixVectorMul(viewport_matrix,v_projected,4)
        v_result = HomToCart(v_result,4)
        
        projected_vertices.append(v_result[:3])
        
    return projected_vertices


def draw_world_axes(screen, view_matrix, projection_matrix, viewport_matrix):
    world_axes = [
        ([0, 0, 0, 1], [1, 0, 0, 1], (255, 0, 0)),  
        ([0, 0, 0, 1], [0, 1, 0, 1], (0, 255, 0)), 
        ([0, 0, 0, 1], [0, 0, 1, 1], (0, 0, 255))  
    ]

    for start, end, color in world_axes:
        
        start_transformed = MatrixVectorMul(view_matrix, start, 4)
        start_projected = MatrixVectorMul(projection_matrix, start_transformed, 4)
        start_projected = HomToCart(start_projected, 4)
        start_projected.append(1)        
        start_result = MatrixVectorMul(viewport_matrix, start_projected, 4)


        end_transformed = MatrixVectorMul(view_matrix, end, 4)
        end_projected = MatrixVectorMul(projection_matrix, end_transformed, 4)
        end_projected = HomToCart(end_projected, 4)
        end_projected.append(1)
        end_result = MatrixVectorMul(viewport_matrix, end_projected, 4)

        pygame.draw.line(screen, color, (start_result[0], start_result[1]), (end_result[0], end_result[1]), 2)

  
def project_point(point, viewport_matrix):
    point_homogeneous = point + [0]
    v_result = MatrixVectorMul(viewport_matrix,point_homogeneous,4)
     
    return v_result[:3]
  




def render_wireframe(screen, mesh,view_matrix, model_matrix, projection_matrix, viewport_matrix, light_direction):

    screen.fill(BLACK)
    projected_vertices = apply_transformations(mesh,view_matrix, model_matrix, projection_matrix, viewport_matrix)    # if len(projected_vertices)  == 4 :
    transformed_vertices = mesh.transform(model_matrix)

    for face in mesh.faces:
        v0 = transformed_vertices[face[0]]
        v1 = transformed_vertices[face[1]]
        v2 = transformed_vertices[face[2]]  
        
        normal = calculate_normal(v0, v1, v2)
        normal = Normalize(normal,3)
        light_direction_final = Normalize(light_direction,3)
        view_direction = Subtraction(v0, 3, camera_position, 3)
        
        if DotProduct(normal, 3, view_direction, 3) <= 0:
            intensity = diffuse_light_intensity(normal, light_direction_final)
            color = apply_lighting_to_color([255, 255, 255], intensity)
            
            v0 = projected_vertices[face[0]]
            v1 = projected_vertices[face[1]]
            v2 = projected_vertices[face[2]]
        
            pygame.draw.polygon(screen, color, [(v0[0], v0[1]), (v1[0], v1[1]), (v2[0], v2[1])])
                
            pygame.draw.line(screen, RED, (v0[0], v0[1]), (v1[0], v1[1]), 2)
            pygame.draw.line(screen,RED, (v1[0], v1[1]), (v2[0], v2[1]), 2)
            pygame.draw.line(screen, RED, (v2[0], v2[1]), (v0[0], v0[1]), 2)
        
    debugRenderer.displayMatrix(rotation_matrix, 50, 50, "Matrice de Rotation")
    debugRenderer.displayMatrix(model_matrix, 50, 200, "Matrice de Modèle")
    debugRenderer.displayVector(euler, 50, 350, "Euler")
    debugRenderer.displayEuler(exponentielMap[0],exponentielMap[1], 50, 500,"Exponentiel map")
    debugRenderer.displayVector(rotation ,400,50, "rotation")
    debugRenderer.displayVector(target_angles ,400,150, "target rotation")
    debugRenderer.displayVector(quaternions, 600, 200, "quaternions")
    debugRenderer.displayText(projection, 600, 250)
    debugRenderer.displayText(mode, 600, 300)
    debugRenderer.displayVector(camera_position, 700, 300,"camera")
    
    
    



font = pygame.font.Font(None, 15)
debugRenderer = DebugRenderer(screen, font)
scale= 1
rotation = [0,0,0]
translation = [0,0,0]
animation_active = False  
animation_active_Exp = False
animation_active_Qua = False
Ortho = False
target_angles = [0, 0, 0]



animation_duration2 = 5
t = 0
target_quaternion = [1,0,0,0]
mode = "camera"

target_angleExp = 0 


camera_position = [0, 0, 0]
camera_sensitivity = 0.03
movement_speed = 0.06

v1 = [1, 0, 0]  
v2 = [0, 1, 0] 
v3 = [0, 0, 1]

yaw = 0
pitch = 0


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                mode = "object" if mode == "camera" else "camera"

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        Ortho = not Ortho
    if keys[pygame.K_SPACE]:
        animation_active = True
        rotation2 = rotation[:]
        t= 0
    if keys[pygame.K_p]:
        animation_active_Qua = True
        quaternions2 = quaternions[:]
        t= 0
    if keys[pygame.K_o]:
        animation_active_Exp = True
        exponentielMap2 = exponentielMap[:]
        t= 0
    if keys[pygame.K_UP]:
        scale += 0.01
    if keys[pygame.K_DOWN]:
        scale -= 0.01
        
    if mode == "camera":
        handle_camera_controls(keys, camera_position, v1, v2 ,v3,movement_speed)
    elif mode == "object":
        handle_object_controls(keys, rotation, translation)
        
    #lerp euler
    if animation_active : 
        t += 1.0 / 60.0 / animation_duration2
        rotation = lerp_euler(rotation2, target_angles, t)
        if t >= 1:
            rotation = target_angles[:]
            animation_active = False
            t= 0

    if Ortho :
        projection_matrix = Scene.projectionMatrixOrtho(-6, 6, -8, 8, -1, 1)
        projection = "projection : Orthograpic"
    else :
        projection = "projection : Perspective"
        projection_matrix = Scene.projectionMatrixPersp(math.radians(70),0.1,100,600/800)
    
    
    view_matrix = Scene.viewMatrix(v1, v2, v3, camera_position)
    viewport_matrix = Scene.viewportMatrix(0, 0, 800, 600,0,1)

    # Orientation
    cubeMesh = TriangleMesh(vertices, faces)
    cubeMesh.SetRotationMatrix(rotation)
    cubeMesh.modelMatrix(scale, translation)
    
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    yaw = mouse_dx * camera_sensitivity
    # pitch = mouse_dy * camera_sensitivity

    # Limiter le pitch pour éviter le retournement
    pitch = max(-math.pi / 2, min(math.pi / 2, pitch))

    yaw_axis = v2
    pitch_axis = v1
    
    v1 = rotate_vector(v1, yaw, yaw_axis) 
    v3 = rotate_vector(v3, yaw, yaw_axis)
    # v2 = rotate_vector(v2, pitch, pitch_axis) 
    # v3 = rotate_vector(v3, pitch, pitch_axis)


    
    
    rotation_matrix = cubeMesh.rotationMatrix
    model_matrix = cubeMesh.modelMatrixRes

    euler = MatrixToEuler(rotation_matrix)
    exponentielMap = getExponentialMap(rotation_matrix)  
    quaternions = ExpMapToQuaternion(exponentielMap[1],exponentielMap[0])
    
    #LERP
    eulerMatrix = eulerToMatrix(euler[0],euler[1],euler[2])

    if animation_active_Qua:
        t += 1.0 / 60.0 / animation_duration2
        quaternions = SlerpQuat(quaternions2, target_quaternion, t)
        rotation = QuaternionToAcardanAngles(quaternions)
        if t >= 1:
            animation_active_Qua = False 
            t=0

   
    if animation_active_Exp:
        t += 1.0 / 60.0 / animation_duration2 
        exponentielMap[0] = (1 - t) * exponentielMap2[0] + t * target_angleExp
        rotation_matrixExp = ExpMapToMatrix(exponentielMap[0], exponentielMap2[1])
        rotation = matrixToAcardanAngles(rotation_matrixExp)

        if t >= 1:
            animation_active_Exp = False
            t=0



    


    # print(rotation_matrix3)
    # print("2" ,quaternions)
    
            
    render_wireframe(screen, cubeMesh,view_matrix, model_matrix, projection_matrix, viewport_matrix,light_direction)
    
    draw_world_axes(screen, view_matrix, projection_matrix, viewport_matrix)

    pygame.display.flip()
   
    clock.tick(60)

pygame.quit()