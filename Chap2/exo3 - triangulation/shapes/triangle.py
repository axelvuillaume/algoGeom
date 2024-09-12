import pygame
from const import SELECTED_TRIANGLE_COLOR, TRIANGLE_COLOR, TRIANGLE_LINE_SIZE, SELECTED_TRIANGLE_BORDER_SIZE

def is_left(A, B, P):
    AB = ((B[0] - A[0]), (B[1] - A[1]))
    AP = ((P[0] - A[0]), (P[1] - A[1]))

    Vx = AB[0]
    Vy = AB[1]
    Wx = AP[0]
    Wy = AP[1]

    current_result = Vx * Wy - Vy * Wx
    
    return current_result > 0

class Triangle:
    def __init__(self, triangle_dots = []):
        self.selected = False
        self.triangle_dots = triangle_dots
        self.triangle_points = []
        for dot in triangle_dots:
            self.triangle_points.append(dot.center)

    def draw(self, surface):
        if (len(self.triangle_points) > 2):
            if (self.selected):
                pygame.draw.polygon(surface, SELECTED_TRIANGLE_COLOR, self.triangle_points, TRIANGLE_LINE_SIZE + SELECTED_TRIANGLE_BORDER_SIZE)
            pygame.draw.polygon(surface, TRIANGLE_COLOR, self.triangle_points, TRIANGLE_LINE_SIZE)

    def is_inside(self, dot):
        point = dot.center
        total_points_number = len(self.triangle_points)
        if (total_points_number > 2):
            is_positif = None
            P = point
            for index in range(len(self.triangle_points)):
                indexA = index % total_points_number
                indexB = (index + 1) % total_points_number

                A = self.triangle_points[indexA]
                B = self.triangle_points[indexB]

                current_is_positif = is_left(A, B, P)

                if (is_positif is None):
                    is_positif = current_is_positif
                elif (current_is_positif != is_positif):
                    return False

            return True
        else:
            print("Not enough points to be a polygon")
            return False
