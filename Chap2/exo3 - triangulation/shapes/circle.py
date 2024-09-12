import pygame

BLUE = (0, 0, 255)

class Circle:
    def __init__ (self, center, radius):
        self.center = center
        self.radius = radius
        
    def draw(self,surface):
        if (self.center is not None):
            pygame.draw.circle(surface, BLUE, self.center, self.radius,2)