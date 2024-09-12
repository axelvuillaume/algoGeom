import pygame
import sys

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

# Classe Point
class Point:
    def __init__(self, pos, radius):
        self.pos = pos  
        self.radius = radius  
        self.color = current_color  

    def draw(self, surface):
        """Dessine le cercle sur la surface donnée."""
        if self.pos:  # Vérifie si self.pos n'est pas None
            pygame.draw.circle(surface, self.color, self.pos, self.radius)


class Polygon:
    def __init__(self, points):
        self.points = points
        self.color = current_color
        

    def draw(self, surface):
        """Dessine le polygone sur la surface donnée."""
        if len(self.points) > 2:
            pygame.draw.polygon(surface, self.color, self.points)

    def change_color(self, new_color):
        """Change la couleur du polygone."""
        self.color = new_color
        
    def point_in_polygon(self, point):
        count=0
        num_vertices = len(self.points)
        x, y = point[0], point[1]
        inside = True
    
        p1 = self.points[0]
    
        # Loop through each edge in the polygon
        for i in range(1, num_vertices + 1):
            # Get the next point in the polygon
            p2 = self.points[i % num_vertices]
    
            # Check if the point is above the minimum y coordinate of the edge
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
        
    # def is_convex(self):
    #     bool = True
    #     for i in range(len(self.points)):
    #             u = (self.points[(i+2)%len(self.points)][0] - self.points[(i+1)%len(self.points)][0], self.points[(i+2)%len(self.points)][1] - self.points[(i+1)%len(self.points)][1])
    #             v = (self.points[(i+1)%len(self.points)][0] - self.points[i][0], self.points[(i+1)%len(self.points)][1] - self.points[i][1])

                
    #             if (u[0]*v[1] - u[1]*v[0] < 0 ) : 
    #                 print (u[0]*v[1] - u[1]*v[0])
    #                 bool == False
        
    #     print (bool)
    #     return bool
    
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
        self.points = Point(self.posPoint, 10)

    def handle_events(self):
        """Gère les événements du clavier et de la souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    self.sommets.append(pos)
                    print (self.poly.is_convex())
                elif event.button == 3:
                    self.posPoint = pygame.mouse.get_pos()
                    self.points = Point(self.posPoint, 10)
                    print(self.poly.point_in_polygon(self.posPoint))

    def run(self):
        """Boucle principale de l'application."""
        while self.running:
            # Gérer les événements
            self.handle_events()

            # Effacer l'écran
            screen.fill(WHITE)

            # Dessiner le polygone
            self.poly.draw(screen)
            
            self.points.draw(screen)

            # Rafraîchir l'écran
            pygame.display.flip()

        # Quitter Pygame proprement
        pygame.quit()
        sys.exit()

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()
