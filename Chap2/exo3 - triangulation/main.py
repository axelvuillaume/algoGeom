import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, DEFAULT_STARTING_ALGO_INDEX
from const import WHITE
from algo import naiveTriangulation,slowDelaunay, voronoi, extremeEdges, jarvisMarch, grahamScan

# Classe principale pour gérer le jeu
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Triangulation")

        pygame.key.set_repeat(500, 50)


        self.running = True

        self.algo = [naiveTriangulation(self.screen), slowDelaunay(self.screen), voronoi(self.screen), extremeEdges(self.screen), jarvisMarch(self.screen), grahamScan(self.screen)]
        self.algo_index = DEFAULT_STARTING_ALGO_INDEX

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Gérer les événements clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    print("Algo 1 selected")
                    self.algo_index = 0
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    print("Algo 2 selected")
                    self.algo_index = 1 % len(self.algo)
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    print("Algo 3 selected")
                    self.algo_index = 2 % len(self.algo)
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    print("Algo 4 selected")
                    self.algo_index = 3 % len(self.algo)
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    print("Algo 5 selected")
                    self.algo_index = 4 % len(self.algo)       
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    print("Algo 6 selected")
                    self.algo_index = 5 % len(self.algo)               
                else:
                    self.algo[self.algo_index].handle_events(event)
            else:
                    self.algo[self.algo_index].handle_events(event)

    def draw(self):
        self.screen.fill(WHITE)
        self.algo[self.algo_index].draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()

        # Quitter pygame
        pygame.quit()
        sys.exit()

# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
