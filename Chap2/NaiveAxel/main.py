import random
import sys
from collections import OrderedDict
from utils import *
import pygame

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
current_color = BLUE


# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Interactions avec Classes en Pygame')


class App:
    def __init__(self):
        self.running = True
        self.points = []
        self.sorted_polygon = []
        self.triangulation = []
        
        for i in range(10):
            posX = random.randint(100,700)
            posY = random.randint(100,500)
            self.points.append(Point(posX, posY))

    
        

    def handle_events(self):
        """Gère les événements du clavier et de la souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                   
                    listP = Function.ExtremeEdges(self.points)
                
                    sortedList = Function.sortVertices(listP)
                    self.sorted_polygon = [(point.x, point.y) for point in sortedList]
                    self.triangulation = Function.TriangulatePolygon(self.points)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    print(pygame.mouse.get_pos())
               
                    

    def run(self):
        """Boucle principale de l'application."""
        while self.running:
            # Gérer les événements
            self.handle_events()

            # Effacer l'écran
            screen.fill(WHITE)

            
            for point in self.points:
                point.draw(screen)
                
            for triangle in self.triangulation:
               triangle.draw(screen)
                
                
            
                
            # if self.sorted_polygon:
            #     pygame.draw.polygon(screen, BLUE, self.sorted_polygon, 2)
            
                
            
            
            
            # Rafraîchir l'écran
            pygame.display.flip()
        



# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()