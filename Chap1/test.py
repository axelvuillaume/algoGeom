import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Interactions avec Classes en Pygame')

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Classe Cercle
class Circle:
    def __init__(self, pos, radius, color):
        self.pos = pos  # Position (x, y)
        self.radius = radius  # Rayon
        self.color = color  # Couleur

    def draw(self, surface):
        """Dessine le cercle sur la surface donnée."""
        pygame.draw.circle(surface, self.color, self.pos, self.radius)

# Classe Rectangle
class Rectangle:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = 5  # Vitesse de déplacement

    def draw(self, surface):
        """Dessine le rectangle sur la surface donnée."""
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        """Déplace le rectangle selon la direction donnée (LEFT, RIGHT, UP, DOWN)."""
        if direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed
        elif direction == "UP":
            self.y -= self.speed
        elif direction == "DOWN":
            self.y += self.speed

    def change_color(self, new_color):
        """Change la couleur du rectangle."""
        self.color = new_color

# Gestionnaire principal de l'application
class App:
    def __init__(self):
        self.running = True
        self.rect = Rectangle(350, 250, 100, 50, RED)  # Le rectangle commence en rouge
        self.circles = []  # Liste pour stocker les cercles

    def handle_events(self):
        """Gère les événements du clavier et de la souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Changer la couleur du rectangle avec les touches
                elif event.key == pygame.K_r:
                    self.rect.change_color(RED)  # Met à jour la couleur du rectangle
                elif event.key == pygame.K_g:
                    self.rect.change_color(GREEN)
                elif event.key == pygame.K_b:
                    self.rect.change_color(BLUE)
                # Déplacer le rectangle avec les touches fléchées
                elif event.key == pygame.K_LEFT:
                    self.rect.move("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.rect.move("RIGHT")
                elif event.key == pygame.K_UP:
                    self.rect.move("UP")
                elif event.key == pygame.K_DOWN:
                    self.rect.move("DOWN")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    pos = pygame.mouse.get_pos()
                    # Ajouter un nouveau cercle à la position de la souris
                    self.circles.append(Circle(pos, 20, self.rect.color))  # Utiliser la couleur actuelle du rectangle

    def run(self):
        """Boucle principale de l'application."""
        while self.running:
            # Gérer les événements
            self.handle_events()

            # Effacer l'écran
            screen.fill(WHITE)

            # Dessiner tous les cercles
            for circle in self.circles:
                circle.draw(screen)

            # Dessiner le rectangle mobile
            self.rect.draw(screen)

            # Rafraîchir l'écran
            pygame.display.flip()

        # Quitter Pygame proprement
        pygame.quit()
        sys.exit()

# Lancer l'application
if __name__ == "__main__":
    app = App()
    app.run()
