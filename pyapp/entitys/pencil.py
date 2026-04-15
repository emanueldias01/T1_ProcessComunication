from entitys.tool import Tool

class Pencil(Tool):
    def __init__(self, app):
        super().__init__(app)
        self.is_painting = False
        self.last_board_pos = None

    def on_mouse_down(self, event, board_x, board_y):
        if event.button == 1:
            self.is_painting = True
            self.last_board_pos = (board_x, board_y)
            self.app.draw_line(board_x, board_y, board_x, board_y, self.app.current_color)

    def on_mouse_up(self, event):
        if event.button == 1:
            self.is_painting = False
            self.last_board_pos = None

    def on_mouse_motion(self, event, board_x, board_y, mouse_x, mouse_y):
        if self.is_painting and self.last_board_pos:
            self.app.draw_line(self.last_board_pos[0], self.last_board_pos[1], board_x, board_y, self.app.current_color)
            self.last_board_pos = (board_x, board_y)