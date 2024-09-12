import pygame
from const import SLOW_DELAUNAY_BACKGROUND_COLOR, WHITE, TITLE_MARGIN_TOP, POLYGON_COLOR, POLYGON_LINE_WIDTH
from config import SCREEN_WIDTH
from utils import generate_random_dots, get_convex_hull_points, FindCircumcenter, detectIllegalEdge
from shapes import Triangle, Circle
import math 

class slowDelaunay : 
    def __init__(self, screen):
        self.screen = screen

        self.current_state = 0

        self.font = pygame.font.Font(None, 74)

        self.dots = []
        self.convex_hull_dots = []
        self.polygon_points = []
        self.remaining_dots = set()
        self.current_dot = None
        self.current_triangle = None
        self.centerCircum = []
        self. finalDots = []

        self.triangulation = []
        self.triangulationFlip = []

    def handle_events(self, event):
        # Gérer les clics de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
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
        self.current_dot = None
        self.current_triangle = None
        
        self.centerCircum = []
        self.triangulationFlip = []
        self.finalDots = []

        self.triangulation = []

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
            case 3:
                print("link all hull points in one")
                A = self.convex_hull_dots[0]
                A.selected = False
                self.remaining_dots.remove(A)
                C = None
                for i in range(1, len(self.convex_hull_dots) - 2):
                    B = self.convex_hull_dots[i]
                    C = self.convex_hull_dots[i + 1]

                    B.selected = False

                    self.triangulation.append(Triangle([A, B, C]))
                    self.remaining_dots.remove(B)
                if C is not None:
                    self.remaining_dots.remove(C)
            case 4:
                print("chose a remaining dot")
                if (self.current_dot is not None):
                    self.current_dot.selected = False
                self.current_dot = self.remaining_dots.pop()
                self.current_dot.selected = True
            case 5:
                print("find the triangle that contain this dot")
                if self.current_triangle is not None:
                    self.current_triangle.selected = False
                for triangle in self.triangulation:
                    if triangle.is_inside(self.current_dot):
                        triangle.selected = True
                        self.current_triangle = triangle
                        break
            case 6:
                print("add 3 new triangle with the current point")
                A = self.current_dot
                for i in range(len(self.current_triangle.triangle_dots)):
                    B = self.current_triangle.triangle_dots[i]
                    C = self.current_triangle.triangle_dots[(i + 1) % len(self.current_triangle.triangle_dots)]
                    self.triangulation.append(Triangle([A, B, C]))
                    self.triangulationFlip.append((A, B, C))
                    
                self.triangulation.remove(self.current_triangle)
                if len(self.remaining_dots) > 0:
                    self.current_state = 3
            case 7:
                print("clean selected shapes")
                self.current_triangle.selected = False
                self.current_dot.selected = False
            
            case 8:
                triangle = self.triangulationFlip.pop()
                A, B, C = triangle[0], triangle[1], triangle[2]
                centerT = FindCircumcenter(A, B, C)
                radius = math.sqrt((centerT[0] - A.center[0]) ** 2 + (centerT[1] - A.center[1]) ** 2)
                print(radius, centerT[0], centerT[1])
                self.centerCircum.append(Circle(centerT, radius))
        
                print(detectIllegalEdge(triangle,self.dots ,radius,centerT,self.triangulationFlip))
                
                if len(self.triangulationFlip) > 0:
                    self.current_state = 7
                    
                
            case 9:
              
                    
                print(len(self.triangulationFlip))
                
            case _:
                pass

    def draw(self):
        self.screen.fill(SLOW_DELAUNAY_BACKGROUND_COLOR)

        text_surface = self.font.render('Slow Delaunay', True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH / 2, TITLE_MARGIN_TOP + text_rect[3] / 2)
        self.screen.blit(text_surface, text_rect)

        if (len(self.polygon_points) > 2):
            pygame.draw.polygon(self.screen, POLYGON_COLOR, self.polygon_points, POLYGON_LINE_WIDTH)

        for triangle in self.triangulation:
            triangle.draw(self.screen)

        for dot in self.dots:
            dot.draw(self.screen)
            
            
        for circle in self.centerCircum :
            circle.draw(self.screen)
