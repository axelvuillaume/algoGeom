import pygame
import random
import sys
from collections import OrderedDict

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Interactions avec Classes en Pygame')


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
current_color = BLUE



class Fonction :
    
    def compare_points(p):
        """Comparer les points en fonction de x, puis de y."""
        return (p.x, p.y)
    
    
    def remove_duplicates(points):
        seen = set()
        unique_points = []
        for point in points:
            if (point.x, point.y) not in seen:
                unique_points.append(point)
                seen.add((point.x, point.y))
        return unique_points
    
    
    def sortVertices(listP):
        finalList = Fonction.remove_duplicates(listP)
        for point in finalList:
                        print(point.x, point.y)
                        
        return sorted(finalList, key=Fonction.compare_points)
        
        

    #Tri marche pas
    def ExtremeEdges(points):
        listP = []
        for i in range(len(points)):
            for j in range(len(points)):
                if i == j:
                    continue
                
                all_same_side = True
                is_positif = None
                
                A = points[i]
                B = points[j]
                for index in range(len(points)):
                    
                    if index == i or index == j:
                        continue
                    
                    P = points[index]

                    AB = (B.x - A.x, B.y - A.y)
                    AP = (P.x - A.x, P.y - A.y)

                    Vx = AB[0]
                    Vy = AB[1]
                    Wx = AP[0]
                    Wy = AP[1]

                    current_result = Vx * Wy - Vy * Wx
                    current_is_positif = current_result > 0

                    if is_positif is None:
                        is_positif = current_is_positif
                    elif current_is_positif != is_positif:
                        all_same_side = False
                
                if all_same_side: 
                    listP.append(A)
                    listP.append(B)

        return listP 
                

    def GetLower(points):
        lowest_y_point = points[0]
        for point in points[1:]:
            if point.y < lowest_y_point.y:
                lowest_y_point = point
        return lowest_y_point
            
        
        
    def JarvisMarch(points):
        startP = Fonction.GetLower(points)
        
        return True
    
# Classe Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def draw(self, surface):
        """Dessine le cercle sur la surface donnée."""
        pygame.draw.circle(surface, BLUE, (self.x,self.y), 5)


class App:
    def __init__(self):
        self.running = True
        self.points = []
        self.sorted_polygon = []
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
                   
                    listP = Fonction.ExtremeEdges(self.points)
                    sortedList = Fonction.sortVertices(listP)
                    self.sorted_polygon = [(point.x, point.y) for point in sortedList]
               
                    
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print ("Press")

    def run(self):
        """Boucle principale de l'application."""
        while self.running:
            # Gérer les événements
            self.handle_events()

            # Effacer l'écran
            screen.fill(WHITE)

            
            for point in self.points:
                point.draw(screen)
            
            Fonction.ExtremeEdges(self.points)
            
            
            
            if self.sorted_polygon:
                pygame.draw.polygon(screen, BLUE, self.sorted_polygon, 2)

            
            # Rafraîchir l'écran
            pygame.display.flip()

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()
