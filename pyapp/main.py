import socket

import pygame
import math
from pixelHubSocketTCP import PixelHubSocketTCP

from pixel import Pixel

# SOCKET

pixelHub = PixelHubSocketTCP()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Board")
clock = pygame.time.Clock()

CANVAS_SIZE = 20
canvas_surface = pygame.Surface((CANVAS_SIZE, CANVAS_SIZE))
canvas_surface.fill("white")

# Posição central da Câmera (em coordenadas do Canvas)
pos = pygame.Vector2(CANVAS_SIZE / 2, CANVAS_SIZE / 2)
zoom = 20.0 

tool = "pencil"
current_color = pygame.Color("black")

is_painting = False
is_panning = False
last_canvas_pos = None
last_mouse_pos = None

pixelBuffer = []

def draw_bresenham(surface, color, x0, y0, x1, y1):
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < CANVAS_SIZE and 0 <= y0 < CANVAS_SIZE:
            surface.set_at((x0, y0), color)

            ## Enviar para outra função
            pixelBuffer.append(Pixel(x0, y0, 0x000000))
            print(x0, y0)
            pixelHub.send_pixels(pixelBuffer)
            pixelBuffer.clear()
        
        if x0 == x1 and y0 == y1:
            break
            
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def screen_to_canvas(screen_x, screen_y, pos_x, pos_y, current_zoom):
    visible_w = WIDTH / current_zoom
    visible_h = HEIGHT / current_zoom
    
    left = pos_x - visible_w / 2
    top = pos_y - visible_h / 2
    
    # Mantém como float para cálculos de câmera precisos
    canvas_x = left + (screen_x / current_zoom)
    canvas_y = top + (screen_y / current_zoom)
    
    return canvas_x, canvas_y


## GameLoop
running = True

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Coordenadas do canvas sob o mouse
    cx_float, cy_float = screen_to_canvas(mouse_x, mouse_y, pos.x, pos.y, zoom)
    
    # Coordenadas para desenhar pixels
    canvas_x, canvas_y = int(cx_float), int(cy_float)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pixelHub.disconnect()
            running = False
            
        elif event.type == pygame.KEYDOWN:
            key = event.unicode.lower()
            if key in ['w', 'b']: tool = "pencil"
            elif key == 'e': tool = "eraser"
            elif key in ['i', 'k']: tool = "dropper"
            elif key in ['h', ' ']: tool = "pan"
            
            # cores
            elif event.key == pygame.K_1: current_color = pygame.Color("#3772FF")
            elif event.key == pygame.K_2: current_color = pygame.Color("#ef2d56")
            elif event.key == pygame.K_3: current_color = pygame.Color("#2fbf71")
            elif event.key == pygame.K_4: current_color = pygame.Color("#000000")

        elif event.type == pygame.MOUSEWHEEL:
            old_zoom = zoom
            zoom += event.y * 0.2 * zoom 
            zoom = max(1.0, min(zoom, 100.0))
            
            if zoom != old_zoom:
                pos.x = cx_float + (WIDTH / 2 - mouse_x) / zoom
                pos.y = cy_float + (HEIGHT / 2 - mouse_y) / zoom

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if tool == "pan":
                    is_panning = True
                    last_mouse_pos = (mouse_x, mouse_y)
                elif tool == "dropper":
                    if 0 <= canvas_x < CANVAS_SIZE and 0 <= canvas_y < CANVAS_SIZE:
                        current_color = canvas_surface.get_at((canvas_x, canvas_y))
                else: 
                    is_painting = True
                    last_canvas_pos = (canvas_x, canvas_y)
                    draw_color = pygame.Color("white") if tool == "eraser" else current_color
                    draw_bresenham(canvas_surface, draw_color, canvas_x, canvas_y, canvas_x, canvas_y)
            
            elif event.button == 2: 
                is_panning = True
                last_mouse_pos = (mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                is_painting = False
                is_panning = False
            elif event.button == 2:
                is_panning = False

        elif event.type == pygame.MOUSEMOTION:
            if is_panning and last_mouse_pos:
                dx = mouse_x - last_mouse_pos[0]
                dy = mouse_y - last_mouse_pos[1]
                pos.x -= dx / zoom  
                pos.y -= dy / zoom
                last_mouse_pos = (mouse_x, mouse_y)
                
            elif is_painting and last_canvas_pos:
                draw_color = pygame.Color("white") if tool == "eraser" else current_color
                draw_bresenham(canvas_surface, draw_color, last_canvas_pos[0], last_canvas_pos[1], canvas_x, canvas_y)
                last_canvas_pos = (canvas_x, canvas_y)

    screen.fill("#2a2a2a")

    visible_w = WIDTH / zoom
    visible_h = HEIGHT / zoom
    left = pos.x - visible_w / 2
    top = pos.y - visible_h / 2

    sub_rect = pygame.Rect(math.floor(left), math.floor(top), math.ceil(visible_w) + 1, math.ceil(visible_h) + 1)
    
    canvas_rect = canvas_surface.get_rect()
    clip_rect = sub_rect.clip(canvas_rect)

    if clip_rect.width > 0 and clip_rect.height > 0:
        visible_piece = canvas_surface.subsurface(clip_rect)
        
        scaled_w = int(clip_rect.width * zoom)
        scaled_h = int(clip_rect.height * zoom)
        scaled_piece = pygame.transform.scale(visible_piece, (scaled_w, scaled_h))
        
        screen_x = (clip_rect.left - left) * zoom
        screen_y = (clip_rect.top - top) * zoom
        
        screen.blit(scaled_piece, (screen_x, screen_y))

    # Preview do Mouse
    if 0 <= canvas_x < CANVAS_SIZE and 0 <= canvas_y < CANVAS_SIZE and not is_panning:
        preview_x = (canvas_x - left) * zoom
        preview_y = (canvas_y - top) * zoom
        overlay = pygame.Surface((int(zoom), int(zoom)), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) 
        screen.blit(overlay, (preview_x, preview_y))
        pygame.draw.rect(screen, "white", (preview_x, preview_y, int(zoom), int(zoom)), 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
