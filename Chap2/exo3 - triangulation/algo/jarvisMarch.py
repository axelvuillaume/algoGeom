import pygame
from const import JARVISMARCH_BACKGROUND_COLOR, WHITE, TITLE_MARGIN_TOP, POLYGON_COLOR, POLYGON_LINE_WIDTH, ORANGE
from config import SCREEN_WIDTH
from utils import generate_random_dots, jarvis_march, lowest_dot, is_left
from shapes import Triangle


class jarvisMarch:
    def __init__(self, screen):
        self.screen = screen

        self.current_state = 0

        self.font = pygame.font.Font(None, 74)

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.point_on_hull = None
        self.start =None
        self.endpoint = None
        self.test_point = None
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
        self.point_on_hull = None
        self.start =None
        self.endpoint = None
        self.test_point = None
        self.i = 0

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
                self.point_on_hull = self.start
                
            case 3:
                print("transit  3")
                self.convex_hull_dots.append(self.point_on_hull)
                self.endpoint = self.dots[0] if self.dots[0] != self.point_on_hull else self.dots[1]  
                self.point_on_hull.selected = True              
            case 4 :
                print("transit  4")
                # for i in range(len(self.dots)):
                self.test_point = self.dots[self.i]
                self.test_point.selected = True
                if is_left(self.point_on_hull.center, self.endpoint.center, self.dots[self.i].center) > 0:
                    self.endpoint = self.dots[self.i]
            
            case 5 :
                print("transit 5")
                print(self.i)
                self.test_point.selected = False
                if self.i < len(self.dots)-1 :
                   
                    self.i += 1
                    self.current_state = 3
                else :  
                    self.point_on_hull.selected = False
                    self.test_point = None  
                    self.point_on_hull = self.endpoint
                    
                    
                    
                    if self.point_on_hull == self.start:
                        print("fin")
                        self.current_state = 5
                    else : 
                        self.point_on_hull.selected = False
                        print("next")
                        self.current_state = 2
                        self.i = 1   
                    
                    
            case 6:
                print("get convex hull points")
                # self.convex_hull_dots = jarvis_march(self.dots)

                for dot in self.convex_hull_dots:
                   self.polygon_points.append(dot.center)
                
            case _:
                pass

    def draw(self):
        self.screen.fill(JARVISMARCH_BACKGROUND_COLOR)

        text_surface = self.font.render("Jarvis' March", True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, TITLE_MARGIN_TOP + text_rect[3] / 2)
        self.screen.blit(text_surface, text_rect)

        if (len(self.polygon_points) > 2):
            pygame.draw.polygon(self.screen, ORANGE, self.polygon_points, POLYGON_LINE_WIDTH)


        for dot in self.dots:
            dot.draw(self.screen)

        if self.point_on_hull is not None and  self.endpoint is not None :
            pygame.draw.line(self.screen,WHITE,self.point_on_hull.center,self.endpoint.center,2)
            if self.test_point is not None :
                pygame.draw.line(self.screen,WHITE,self.point_on_hull.center,self.test_point.center,2)
