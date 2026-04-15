from entitys.tool import Tool

class Dropper(Tool):
    def on_mouse_down(self, event, board_x, board_y):
        if event.button == 1:
            if 0 <= board_x < self.app.BOARD_SIZE and 0 <= board_y < self.app.BOARD_SIZE:
                self.app.current_color = self.app.board_surface.get_at((board_x, board_y))
