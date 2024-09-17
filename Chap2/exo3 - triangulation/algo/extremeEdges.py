import pygame
from const import EXTREMEEDGES_BACKGROUND_COLOR, WHITE, TITLE_MARGIN_TOP, POLYGON_COLOR, POLYGON_LINE_WIDTH
from config import SCREEN_WIDTH
from utils import generate_random_dots, get_convex_hull_points
from shapes import Triangle

class extremeEdges:
    def __init__(self, screen):
        self.screen = screen

        self.current_state = 0

        self.font = pygame.font.Font(None, 74)

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.remaining_dots = set()

    def handle_events(self, event):
        # Gérer les clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                # mouse_pos = event.pos
                print("Mouse clicked - next step")
                self.next_state()

        # Gérer les événements clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                print("reset")
                self.reset()
            if event.key == pygame.K_SPACE:
                print("Space clicked - next step")
                self.next_state()
    
    def reset(self):
        self.current_state = 0

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.remaining_dots = set()


    def next_state(self):
        match self.current_state:
            case _:
                pass
        
        self.current_state += 1

        match self.current_state:
            case 1:
                print("generate random dots")
                self.dots = generate_random_dots()
                self.remaining_dots = set(self.dots)
            case 2:
                print("get convex hull points")
                self.convex_hull_dots = get_convex_hull_points(self.dots)

                for dot in self.convex_hull_dots:
                    self.polygon_points.append(dot.center)
            case _:
                pass

    def draw(self):
        self.screen.fill(EXTREMEEDGES_BACKGROUND_COLOR)

        text_surface = self.font.render('Extreme Edge', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, TITLE_MARGIN_TOP + text_rect[3] / 2)
        self.screen.blit(text_surface, text_rect)

        if (len(self.polygon_points) > 2):
            pygame.draw.polygon(self.screen, POLYGON_COLOR, self.polygon_points, POLYGON_LINE_WIDTH)


        for dot in self.dots:
            dot.draw(self.screen)
