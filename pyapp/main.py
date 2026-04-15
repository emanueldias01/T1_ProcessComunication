import time
import threading
import math
import pygame
import argparse

from streams.pixelHubSocketTCP import PixelHubTCP
from streams.pixelHubSocketUDP import PixelHubUDP
from entitys.pixel import Pixel

from entitys.pencil import Pencil
from entitys.eraser import Eraser
from entitys.drooper import Dropper
from entitys.pan import Pan

class PixelCanvasApp:
    def __init__(self, ip, port, udp, udpGroup, udpPort):
        pygame.init()
        
        self.WIDTH, self.HEIGHT = 500, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pixel Board")

        self.BOARD_SIZE = 500
        self.board_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.board_surface.fill("white")

        # camera
        self.pos = pygame.Vector2(self.WIDTH / 2, self.HEIGHT / 2)
        self.zoom = 20.0

        self.pixelHub = PixelHubTCP(ip, port)
        self.is_udp = udp
        if udp:
            self.pixelHubMultiCast = PixelHubUDP(udpGroup, udpPort)

        self.pixelBuffer = []
        self.buffer_lock = threading.Lock()
        self.running = False

        self.current_color = pygame.Color("black")
        
        self.tools = {
            "pencil": Pencil(self),
            "eraser": Eraser(self),
            "dropper": Dropper(self),
            "pan": Pan(self)
        }
        self.active_tool = self.tools["pencil"]
        
        # Pan Global (botão do meio)
        self.global_panning = False
        self.global_last_mouse_pos = None

    def init_sync(self):
        board_data = self.pixelHub.recv_board()
        if board_data:
            for x in range(self.WIDTH):
                for y in range(self.HEIGHT):
                    color = board_data.getColorAt(x, y)
                    self.board_surface.set_at((x, y), color)

    def start_threads(self):
        thread_rp = threading.Thread(target=self.reading_pixels, daemon=True)
        thread_sb = threading.Thread(target=self.sending_pixel_buffer, daemon=True)
        thread_rp.start()
        thread_sb.start()

    def reading_pixels(self):
        while self.running:
            pixels = []
            if self.is_udp:
                pixels = self.pixelHubMultiCast.recv_pixels()
            else:
                pixels = self.pixelHub.recv_pixels()
            
            if pixels:
                for p in pixels:
                    self.board_surface.set_at((p.x, p.y), p.color)
            # para dar efeito de traço sendo gerado
            time.sleep(0.06)

    def sending_pixel_buffer(self):
        while self.running:
            pixels_to_send = []
            with self.buffer_lock:
                if self.pixelBuffer:
                    pixels_to_send = list(self.pixelBuffer)
                    self.pixelBuffer.clear()
            
            if pixels_to_send:
                self.pixelHub.send_pixels(pixels_to_send)        
            time.sleep(0.100)

    def screen_to_board(self, screen_x, screen_y):
        visible_w = self.WIDTH / self.zoom
        visible_h = self.HEIGHT / self.zoom
        
        left = self.pos.x - visible_w / 2
        top = self.pos.y - visible_h / 2
        
        board_x = left + (screen_x / self.zoom)
        board_y = top + (screen_y / self.zoom)
        
        return board_x, board_y

    def draw_line(self, x0, y0, x1, y1, color):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy

        while True:
            if 0 <= x0 < self.WIDTH and 0 <= y0 < self.HEIGHT:
                self.board_surface.set_at((x0, y0), color)

                with self.buffer_lock:
                    self.pixelBuffer.append(Pixel(x0, y0, int(color) >> 8))
            
            if x0 == x1 and y0 == y1:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def handle_events(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        cx_float, cy_float = self.screen_to_board(mouse_x, mouse_y)
        board_x, board_y = int(cx_float), int(cy_float)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                key = event.unicode.lower()
                
                # Troca de Ferramentas
                if key in ['w', 'b']: self.active_tool = self.tools["pencil"]
                elif key == 'e': self.active_tool = self.tools["eraser"]
                elif key in ['i', 'k']: self.active_tool = self.tools["dropper"]
                elif key in ['h', ' ']: self.active_tool = self.tools["pan"]
                
                # Troca cores
                elif event.key == pygame.K_0: self.current_color = pygame.Color("#FFFFFF")
                elif event.key == pygame.K_1: self.current_color = pygame.Color("#000000")
                elif event.key == pygame.K_2: self.current_color = pygame.Color("#ef2d56")
                elif event.key == pygame.K_3: self.current_color = pygame.Color("#2fbf71")
                elif event.key == pygame.K_4: self.current_color = pygame.Color("#3772FF")
                elif event.key == pygame.K_5: self.current_color = pygame.Color("#FFDA37")
                elif event.key == pygame.K_6: self.current_color = pygame.Color("#D346E6")

            elif event.type == pygame.MOUSEWHEEL:
                old_zoom = self.zoom
                self.zoom += event.y * 0.2 * self.zoom 
                self.zoom = max(1.0, min(self.zoom, 100.0))
                
                if self.zoom != old_zoom:
                    self.pos.x = cx_float + (self.WIDTH / 2 - mouse_x) / self.zoom
                    self.pos.y = cy_float + (self.HEIGHT / 2 - mouse_y) / self.zoom

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.global_panning = True
                    self.global_last_mouse_pos = (mouse_x, mouse_y)
                else:
                    self.active_tool.on_mouse_down(event, board_x, board_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.global_panning = False
                    self.global_last_mouse_pos = None
                else:
                    self.active_tool.on_mouse_up(event)

            elif event.type == pygame.MOUSEMOTION:
                # Trata o pan global primeiro
                if self.global_panning and self.global_last_mouse_pos:
                    dx = mouse_x - self.global_last_mouse_pos[0]
                    dy = mouse_y - self.global_last_mouse_pos[1]
                    self.pos.x -= dx / self.zoom  
                    self.pos.y -= dy / self.zoom
                    self.global_last_mouse_pos = (mouse_x, mouse_y)
                else:
                    # Delega para a ferramenta ativa
                    self.active_tool.on_mouse_motion(event, board_x, board_y, mouse_x, mouse_y)

    def render(self):
        self.screen.fill("#2a2a2a")

        visible_w = self.WIDTH / self.zoom
        visible_h = self.HEIGHT / self.zoom
        left = self.pos.x - visible_w / 2
        top = self.pos.y - visible_h / 2

        sub_rect = pygame.Rect(math.floor(left), math.floor(top), math.ceil(visible_w) + 1, math.ceil(visible_h) + 1)
        board_rect = self.board_surface.get_rect()
        clip_rect = sub_rect.clip(board_rect)

        if clip_rect.width > 0 and clip_rect.height > 0:
            visible_piece = self.board_surface.subsurface(clip_rect)
            
            scaled_w = int(clip_rect.width * self.zoom)
            scaled_h = int(clip_rect.height * self.zoom)
            scaled_piece = pygame.transform.scale(visible_piece, (scaled_w, scaled_h))
            
            screen_x = (clip_rect.left - left) * self.zoom
            screen_y = (clip_rect.top - top) * self.zoom
            
            self.screen.blit(scaled_piece, (screen_x, screen_y))

        # Preview do Mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bx_float, by_float = self.screen_to_board(mouse_x, mouse_y)
        board_x, board_y = int(bx_float), int(by_float)

        is_panning_tool = (self.active_tool == self.tools["pan"])
        if 0 <= board_x < self.WIDTH and 0 <= board_y < self.HEIGHT and not self.global_panning and not is_panning_tool:
            preview_x = (board_x - left) * self.zoom
            preview_y = (board_y - top) * self.zoom
            overlay = pygame.Surface((int(self.zoom), int(self.zoom)), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100)) 
            self.screen.blit(overlay, (preview_x, preview_y))
            pygame.draw.rect(self.screen, "white", (preview_x, preview_y, int(self.zoom), int(self.zoom)), 1)

        pygame.display.flip()

    def run(self):
        self.running = True
        self.init_sync()
        self.start_threads()

        while self.running:
            self.handle_events()
            self.render()
            self.clock.tick(60)

        self.pixelHub.disconnect()

        if self.is_udp:
            self.pixelHubMultiCast.disconnect()
        
        pygame.quit()

def main():
    parser = argparse.ArgumentParser(description="Inicia o Pixel Board Client.")
    
    parser.add_argument(
        "--ip", 
        type=str, 
        default="10.10.241.238", 
        help="Endereço IP da máquina servidor"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=5000, 
        help="Porta de conexão do servidor"
    )

    parser.add_argument(
        "--udp", 
        action="store_true"
    )
    
    parser.add_argument(
        "--udpGroup", 
        type=str, 
        default="224.1.1.1"
    )

    parser.add_argument(
        "--udpPort", 
        type=int, 
        default=50003
    )

    args = parser.parse_args()
    
    app = PixelCanvasApp(args.ip, args.port, args.udp, args.udpGroup, args.udpPort)
    app.run()

if __name__ == "__main__":
    main()