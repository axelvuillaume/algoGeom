import pygame
from const import *

class DebugRenderer:
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def displayMatrix(self, matrix, x, y, title):
        text_surface = self.font.render(title, True, WHITE)
        self.screen.blit(text_surface, (x, y))
    
        for i, row in enumerate(matrix):
            matrix_text = ' '.join([f'{value:.2f}' for value in row])
            text_surface = self.font.render(matrix_text, True, WHITE)
            self.screen.blit(text_surface, (x, y + (i + 1) * 20))
    
    def displayVector(self, vector, x, y, title):
        text_surface = self.font.render(title, True, WHITE)
        self.screen.blit(text_surface, (x, y))
        for i, value in enumerate(vector):
            text_surface = self.font.render(f"{value:.2f}", True, WHITE)
            self.screen.blit(text_surface, (x, y + 10 * (i + 1))) 
            
    def displayText(self, text, x, y):
        text_surface = self.font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x, y))
        
    def displayEuler(self, angle, vector, x, y,title):
        text_surface = self.font.render(title, True, WHITE)
        self.screen.blit(text_surface, (x, y))
        # Affiche l'angle
        angle_text = f"Angle: {angle:.2f}°"
        angle_surface = self.font.render(angle_text, True, (255, 255, 255))
        self.screen.blit(angle_surface, (x, y+10))

        # Affiche le vecteur
        vector_text = f"Axis: [{vector[0]:.2f}, {vector[1]:.2f}, {vector[2]:.2f}]"
        vector_surface = self.font.render(vector_text, True, (255, 255, 255))
        self.screen.blit(vector_surface, (x, y + 30))