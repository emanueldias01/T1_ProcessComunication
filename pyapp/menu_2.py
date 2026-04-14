import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu - Pixel Board")
clock = pygame.time.Clock()

# Fontes e Cores
FONT = pygame.font.Font("font/Pixeled.ttf", 16)
TITLE_FONT = pygame.font.SysFont("Arial", 40, bold=True)

COLOR_BG = pygame.Color("#b3b9d1")
COLOR_TEXT = pygame.Color("#111111")
COLOR_BOX_ACTIVE = pygame.Color("#3772FF")
COLOR_BOX_INACTIVE = pygame.Color("#555555")
COLOR_BTN = pygame.Color("#b3b9d1")
COLOR_BTN_HOVER = pygame.Color("#36AEC4")
COLOR_BTN_QUIT = pygame.Color("#b3b9d1")
COLOR_BTN_QUIT_HOVER = pygame.Color("#36AEC4")
img = pygame.image.load("menu.png").convert()
BG_IMAGE = pygame.transform.scale_by(img, 3.9)

class InputBox:
    def __init__(self, x, y, w, h, placeholder_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_BOX_INACTIVE
        self.text = ''
        self.placeholder = placeholder_text
        self.txt_surface = FONT.render(self.placeholder, True, COLOR_BOX_INACTIVE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Se o usuário clicou no retângulo do input box
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_BOX_ACTIVE if self.active else COLOR_BOX_INACTIVE
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass # O enter pode ser tratado depois
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limita o tamanho do texto para caber na caixa
                    if self.txt_surface.get_width() < self.rect.w - 20:
                        self.text += event.unicode
                
                self.update_text_surface()

    def update_text_surface(self):
        # Mostra o texto digitado ou o placeholder se estiver vazio
        if self.text == '':
            self.txt_surface = FONT.render(self.placeholder, True, COLOR_BOX_INACTIVE)
        else:
            self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.txt_surface = FONT.render(self.text, True, COLOR_TEXT)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)
        
        # Draw borders
        border_color = pygame.Color("#dae0ea")
        border_color2 = pygame.Color("#403353")
        border_width = 2
        pygame.draw.line(screen, border_color, self.rect.topleft, self.rect.topright, border_width)  # top
        pygame.draw.line(screen, border_color2, self.rect.bottomleft, self.rect.bottomright, border_width)  # bottom
        pygame.draw.line(screen, border_color, self.rect.topleft, self.rect.bottomleft, border_width)  # left
        pygame.draw.line(screen, border_color2, self.rect.topright, self.rect.bottomright, border_width)  # right
        
        # Centralizar texto
        text_rect = self.txt_surface.get_rect(center=self.rect.center)
        screen.blit(self.txt_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False

def main_menu():
    # Instanciando os elementos de UI
    #input_ip = InputBox(100, 150, 300, 40, "Digite o IP (ex: 127.0.0.1)")
    #input_port = InputBox(100, 220, 300, 40, "Digite a Porta (ex: 5050)")
    
    btn_enter = Button(100, 320, 140, 50, "Entrar", COLOR_BTN, COLOR_BTN_HOVER)
    btn_quit = Button(260, 320, 140, 50, "Sair", COLOR_BTN_QUIT, COLOR_BTN_QUIT_HOVER)

    running = True
    while running:
        screen.blit(BG_IMAGE, (0, 0))

        # Rótulos dos campos
        #ip_label = FONT.render("IP:", True, COLOR_TEXT)
        #screen.blit(ip_label, (100, 120))
        
        #port_label = FONT.render("Porta:", True, COLOR_TEXT)
        #screen.blit(port_label, (100, 190))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            #input_ip.handle_event(event)
            #input_port.handle_event(event)

            if btn_quit.is_clicked(event):
                running = False
                pygame.quit()
                sys.exit()

            if btn_enter.is_clicked(event):
                #ip_value = input_ip.text
                #port_value = input_port.text
                
                print(f"Tentando conectar com IP: {ip_value} e Porta: {port_value}")
                # Aqui você pode salvar esses dados em um arquivo, 
                # ou iniciar o seu outro script usando a biblioteca os/subprocess.
                running = False # Sai do menu após clicar em entrar

        # Atualizar e Desenhar UI
        #input_ip.draw(screen)
        #input_port.draw(screen)
        btn_enter.draw(screen)
        btn_quit.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
    pygame.quit()