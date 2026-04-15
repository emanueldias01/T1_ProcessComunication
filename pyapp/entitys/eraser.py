import pygame
from entitys.pencil import Pencil

class Eraser(Pencil):
    def on_mouse_down(self, event, board_x, board_y):
        if event.button == 1:
            self.is_painting = True
            self.last_board_pos = (board_x, board_y)
            self.app.draw_line(board_x, board_y, board_x, board_y, pygame.Color("white"))

    def on_mouse_motion(self, event, board_x, board_y, mouse_x, mouse_y):
        if self.is_painting and self.last_board_pos:
            self.app.draw_line(self.last_board_pos[0], self.last_board_pos[1], board_x, board_y, pygame.Color("white"))
            self.last_board_pos = (board_x, board_y)