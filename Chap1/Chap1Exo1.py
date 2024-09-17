import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Convexe / Concave')


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
current_color = BLUE
    
class Point:
    def __init__(self, pos, radius):
        self.pos = pos  
        self.radius = radius
        self.statut = ""

    def draw(self, surface):
        if self.statut == 'in' :
            self.color = BLUE
        elif self.statut == 'out':
            self.color = RED
        else :
            self.color = current_color
            
            
        if self.pos:
            pygame.draw.circle(surface, self.color, self.pos, self.radius)
            



class Polygon:
    def __init__(self, points):
        self.points = points
        self.selected = ""
        
    def draw(self, surface):
        if self.selected == 'concave' :
            self.color = BLUE
        elif self.selected == 'convexe':
            self.color = RED
        else :
            self.color = current_color
            
        if len(self.points) > 2:
            pygame.draw.polygon(surface, self.color, self.points,2)
            
    def point_in_polygon_convexe(self, point):
        num_vertices = len(self.points)
        x, y = point[0], point[1]
        
        def cross_product(A, B, P):
            return (B[0] - A[0]) * (P[1] - A[1]) - (B[1] - A[1]) * (P[0] - A[0])

        # Initialiser le signe du premier produit vectoriel
        A = self.points[0]
        B = self.points[1]
        initial_sign = cross_product(A, B, point) > 0
        
        # Vérifier pour chaque segment si le produit vectoriel a le même signe
        for i in range(1, num_vertices):
            A = self.points[i]
            B = self.points[(i + 1) % num_vertices]
            if (cross_product(A, B, point) > 0) != initial_sign:
                return True

        return False

        
    def point_in_polygon(self, point):
        count=0
        num_vertices = len(self.points)
        x, y = point[0], point[1]
        inside = True
    
        p1 = self.points[0]
    
        
        for i in range(1, num_vertices + 1):
            
            p2 = self.points[i % num_vertices]
    
            if y > min(p1[1], p2[1]):
                if y <= max(p1[1], p2[1]):
                    if x <= max(p1[0], p2[0]):
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]
    
                        if p1[0] == p2[0] or x <= x_intersection:
                            count+=1
    
            p1 = p2

        
       
        if ((count%2) == 0):
            return inside
        else:
            return not inside



    def is_convex(self):
        total_points_number = len(self.points)
        if (total_points_number > 2):
            is_positif = None
            for index in range(len(self.points)):
                indexA = index % total_points_number
                indexB = (index + 1) % total_points_number
                indexP = (index + 2) % total_points_number

                A = self.points[indexA]
                B = self.points[indexB]
                P = self.points[indexP]

                AB = ((B[0] - A[0]), (B[1] - A[1]))
                AP = ((P[0] - A[0]), (P[1] - A[1]))

                Vx = AB[0]
                Vy = AB[1]
                Wx = AP[0]
                Wy = AP[1]

                current_result = Vx * Wy - Vy * Wx

              

                current_is_positif = current_result > 0

                if (is_positif is None):
                    is_positif = current_is_positif
                elif (current_is_positif != is_positif):
                    return False

            return True
        else:
            print("Not enough points to be a polygon")
            return False

class App:
    def __init__(self):
        self.running = True
        self.sommets = []
        self.poly = Polygon(self.sommets)
        
        self.posPoint = None
        self.points = Point(self.posPoint, 5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.sommets.append(pos)
                    if self.poly.is_convex():
                        self.poly.selected = 'convexe'
                        print("Convexe")
                    else: 
                        self.poly.selected = 'concave'
                        print("Concave")
                elif event.button == 3:
                    self.posPoint = pygame.mouse.get_pos()
                    self.points = Point(self.posPoint, 5)
                    
                    if not self.poly.is_convex() :
                        if self.poly.point_in_polygon(self.points.pos):
                            self.points.statut = 'out'
                            print("Crossing Method : Dehors")
                        else: 

                            self.points.statut = 'in'
                            print("Crossing Method : Interieur")
                            
                    else :
                        if self.poly.point_in_polygon_convexe(self.points.pos):
                            self.points.statut = 'out'
                            print("Orientation Method : Dehors")
                        else: 

                            self.points.statut = 'in'
                            print("Orientation Method : Interieur")
                        
                        
    def run(self):
        while self.running:
            
            self.handle_events()

            screen.fill(WHITE)

            self.poly.draw(screen)
            
            self.points.draw(screen)
                
            for point in self.sommets:
                pygame.draw.circle(screen, GREEN, point, 4)
            
            pygame.display.flip()

        pygame.quit()
        sys.exit()

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()