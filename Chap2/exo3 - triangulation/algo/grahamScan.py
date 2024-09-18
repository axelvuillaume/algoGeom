import pygame
from const import GRAHAMSCAN_BACKGROUND_COLOR, WHITE, TITLE_MARGIN_TOP, POLYGON_COLOR, POLYGON_LINE_WIDTH, ORANGE
from config import SCREEN_WIDTH
from utils import generate_random_dots, graham_scan,lowest_dot, polar_angle_sort,cross_product
from shapes import Triangle

class grahamScan:
    def __init__(self, screen):
        self.screen = screen

        self.current_state = 0

        self.font = pygame.font.Font(None, 74)

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.hull = []
        self.start =None
        self.endpoint = None
        self.test_point = None
        self.sorted_dots = []
        self.i = 0

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


    def next_state(self):
        match self.current_state:
            case _:
                pass
        
        self.current_state += 1

        match self.current_state:
            case 1:
                print("generate random dots")
                self.dots = generate_random_dots()
            case 2:
                
                self.start = lowest_dot(self.dots)
                self.start.selected = True
                
                self.sorted_dots = polar_angle_sort([dot for dot in self.dots if dot != self.start], self.start)
                
                self.hull = [self.start]
                self.i = 0
                
            case 3:
                if self.i < len(self.sorted_dots):
                    self.current_point = self.sorted_dots[self.i]
                    self.current_point.selected = True
                else :
                    self.current_state = 5 
                            
                 
            case 4 :
                if len(self.hull) > 1 and cross_product(self.hull[-2].center, self.hull[-1].center, self.current_point.center) <= 0:
                    self.hull.pop()
                    self.current_state = 2
                    print("pop")
                    self.current_point.selected = False
                else : 
                    print("add")
                    self.hull.append(self.current_point)
                    self.i += 1
                    self.current_state = 2
                    self.current_point.selected = False
        
            case 6:
                print("get convex hull points")
                # self.convex_hull_dots = jarvis_march(self.dots)

                for dot in self.hull:
                   self.polygon_points.append(dot.center)
                   
            
                
            case _:
                pass
    def draw(self):
        self.screen.fill(GRAHAMSCAN_BACKGROUND_COLOR)

        text_surface = self.font.render("Graham's Scan", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, TITLE_MARGIN_TOP + text_rect[3] / 2)
        self.screen.blit(text_surface, text_rect)

        for dot in self.dots:
            dot.draw(self.screen)


        if len(self.hull) > 1:
            for i in range(1, len(self.hull)):
                pygame.draw.line(self.screen,WHITE,self.hull[i-1].center,self.hull[i].center,2)
                
                

        if (len(self.polygon_points) > 2):
            pygame.draw.polygon(self.screen, ORANGE, self.polygon_points, POLYGON_LINE_WIDTH)



        