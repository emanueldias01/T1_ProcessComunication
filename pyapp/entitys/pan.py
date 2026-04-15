import pygame
from entitys.tool import Tool

class Pan(Tool):
    def __init__(self, app):
        super().__init__(app)
        self.is_panning = False
        self.last_mouse_pos = None

    def on_mouse_down(self, event, board_x, board_y):
        if event.button == 1:
            self.is_panning = True
            self.last_mouse_pos = pygame.mouse.get_pos()

    def on_mouse_up(self, event):
        if event.button == 1:
            self.is_panning = False
            self.last_mouse_pos = None

    def on_mouse_motion(self, event, board_x, board_y, mouse_x, mouse_y):
        if self.is_panning and self.last_mouse_pos:
            dx = mouse_x - self.last_mouse_pos[0]
            dy = mouse_y - self.last_mouse_pos[1]
            self.app.pos.x -= dx / self.app.zoom
            self.app.pos.y -= dy / self.app.zoom
            self.last_mouse_pos = (mouse_x, mouse_y)