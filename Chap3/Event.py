import pygame
import math
from VectorOperation.VectorOperation import *

def move_camera(camera_position, direction, amount):
    """Déplace la caméra dans une direction donnée (v1, v2, v3)"""
    camera_position[0] += direction[0] * amount
    camera_position[1] += direction[1] * amount
    camera_position[2] += direction[2] * amount

def rotate_vector(v, angle, axis):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    axis = Normalize(axis,3) 
    ux, uy, uz = axis
    rotation_matrix = [
        [cos_angle + ux**2 * (1 - cos_angle), ux * uy * (1 - cos_angle) - uz * sin_angle, ux * uz * (1 - cos_angle) + uy * sin_angle],
        [uy * ux * (1 - cos_angle) + uz * sin_angle, cos_angle + uy**2 * (1 - cos_angle), uy * uz * (1 - cos_angle) - ux * sin_angle],
        [uz * ux * (1 - cos_angle) - uy * sin_angle, uz * uy * (1 - cos_angle) + ux * sin_angle, cos_angle + uz**2 * (1 - cos_angle)]
    ]
    return MatrixVector3Mul(rotation_matrix, v,3)

def handle_camera_controls(keys, camera_position, v1, v2, v3,camera_sensitivity):
    if keys[pygame.K_e]:
          camera_position[2] += 0.1
        # move_camera(camera_position, v3, -camera_sensitivity)  # Déplace la caméra vers la gauche
    if keys[pygame.K_a]:
        camera_position[2] -= 0.1
        # move_camera(camera_position, v3, camera_sensitivity)  # Déplace la caméra vers la gauche
    if keys[pygame.K_q]:
        camera_position[0] += 0.1
        # move_camera(camera_position, v1, -camera_sensitivity)  # Déplace la caméra vers la gauche
    if keys[pygame.K_d]:
        camera_position[0] -= 0.1
        # move_camera(camera_position, v1, camera_sensitivity)   # Déplace la caméra vers la droite
    if keys[pygame.K_z]:
        camera_position[1] += 0.1
        # move_camera(camera_position, v2, -camera_sensitivity)   # Déplace la caméra en avant
    if keys[pygame.K_s]:
        camera_position[1] -= 0.1
        # move_camera(camera_position, v2, camera_sensitivity)  # Déplace la caméra en arrière
    
vitesse_object = 0.1
def handle_object_controls(keys, rotation, translation):
    if keys[pygame.K_q]:
        translation[0] -= vitesse_object
    if keys[pygame.K_d]:
        translation[0] += vitesse_object
    if keys[pygame.K_z]:
        translation[1] += vitesse_object
    if keys[pygame.K_s]:
        translation[1] -= vitesse_object
    if keys[pygame.K_m]:
        translation[2] += vitesse_object
    if keys[pygame.K_n]:
        translation[2] -= vitesse_object
    if keys[pygame.K_KP0]:
        rotation[0] += vitesse_object
    if keys[pygame.K_KP1]:
        rotation[0] -= vitesse_object
    if keys[pygame.K_KP2]:
        rotation[1] += vitesse_object
    if keys[pygame.K_KP3]:
        rotation[1] -= vitesse_object
    if keys[pygame.K_KP4]:
        rotation[2] += vitesse_object
    if keys[pygame.K_KP5]:
        rotation[2] -= vitesse_object
