import pygame
from const import EXTREMEEDGES_BACKGROUND_COLOR, WHITE, TITLE_MARGIN_TOP, POLYGON_COLOR, POLYGON_LINE_WIDTH, GREEN , RED
from config import SCREEN_WIDTH
from utils import generate_random_dots, is_extrem_edge,sort_extrem_edges
from shapes import Triangle

class extremeEdges:
    def __init__(self, screen):
        self.screen = screen

        self.current_state = 0

        self.font = pygame.font.Font(None, 74)

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.extrem_edges = []
        self.i = 0
        self.j = 0
        self.edge = 0
        self.sorted_edges = []
        self.colorBon = WHITE

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
        self.extrem_edges = []
        self.colorBon = 0


    def next_state(self):
        match self.current_state:
            case _:
                pass
        
        self.current_state += 1

        match self.current_state:
            case 1:
                print("generate random dots")
                self.dots = generate_random_dots()
                
            case 2 : 
                 
                
                if is_extrem_edge(self.dots, self.i, self.j):
                    self.extrem_edges.append((self.i, self.j))
                    self.colorBon = GREEN
                else : 
                    self.colorBon = RED
                    

                 
            case 3 :
                
                self.colorBon = WHITE
                if self.j < len(self.dots):
                    self.j += 1
                    self.current_state = 1
                if self.j >= len(self.dots):
                    self.i += 1
                    self.j = self.i + 1
                    self.current_state = 1
                    
                    if self.i >= len(self.dots) - 1:
                        self.current_state = 3
                        print("peut etre")
                        
                    
            case 4 :
                
                
                self.sorted_edges = sort_extrem_edges(self.extrem_edges[:])
                self.convex_hull_dots = [self.dots[self.sorted_edges[0][0]]]
                self.current_state = 4
                
            
            case 5 :
                self.convex_hull_dots.append(self.dots[self.sorted_edges[self.edge][1]])
                self.current_state = 5
                    

            case 6 :
                
                if (self.edge) < len(self.sorted_edges)-1:
                    self.edge += 1
                    self.current_state = 4
                    
            case 7:
                print("get convex hull points")
                # self.convex_hull_dots = get_convex_hull_points(self.dots)

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


        for dot in self.dots:
            dot.draw(self.screen)

        if len(self.dots) > 1 and self.j < len(self.dots):
            pygame.draw.line(self.screen,self.colorBon,self.dots[self.i].center,self.dots[self.j].center,2)
        
        
        if len(self.convex_hull_dots) > 1:
            for i in range(1, len(self.convex_hull_dots)):
                pygame.draw.line(self.screen,WHITE,self.convex_hull_dots[i-1].center,self.convex_hull_dots[i].center,2)
               
               
        if (len(self.polygon_points) > 2):
            pygame.draw.polygon(self.screen, POLYGON_COLOR, self.polygon_points, POLYGON_LINE_WIDTH)

