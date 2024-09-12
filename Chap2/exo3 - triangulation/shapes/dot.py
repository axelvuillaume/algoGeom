import pygame
from const import DOT_SIZE, DOT_COLOR, SELECTED_DOT_BORDER_SIZE, SELECTED_DOT_COLOR

class Dot:
    def __init__(self, center, hide = False):
        self.center = center
        self.selected = False
        self.hide = hide

    def draw(self, surface):
        if (self.center is not None and not self.hide):
            if (self.selected):
                pygame.draw.circle(surface, SELECTED_DOT_COLOR, self.center, DOT_SIZE + SELECTED_DOT_BORDER_SIZE)
            pygame.draw.circle(surface, DOT_COLOR, self.center, DOT_SIZE)
