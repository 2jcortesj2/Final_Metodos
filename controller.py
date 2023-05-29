import pygame
import model
import view

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 720, 480

screen = pygame.display.set_mode((WIDTH, HEIGHT)) ####################
pygame.display.set_caption("Snake")

alternate_screen = pygame.Surface((WIDTH, HEIGHT))#########

# Colores
GREEN = (144,175,49)
WHITE = (255, 255, 255)

# Fuente de letra
font_path = "Resources\ConcertOne-Regular.ttf"
font_size = 32
font = pygame.font.Font(font_path, font_size)

# Función para dibujar texto centrado
def draw_text_centered(text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    screen.blit(text_surface, text_rect)

def is_within_rect(pos, rect):
    return rect.collidepoint(pos)

# Cargar la imagen
image_path = r"Resources\NicePng_snake-logo-png_2952520.png"
image = pygame.image.load(image_path)

# Función para dibujar el contenido de la pantalla principal
def main_screen():
    screen.fill(WHITE)
    
    # Dibujar los botones
    rect1 = pygame.Rect(270, 278, 180, 53)
    pygame.draw.rect(screen, GREEN, rect1)
    draw_text_centered("Grabar", font, WHITE, rect1)
    
    rect2 = pygame.Rect(270, 360, 180, 53)
    pygame.draw.rect(screen, GREEN, rect2)
    draw_text_centered("Jugar", font, WHITE, rect2)

    # Dibujar la imagen en la pantalla
    screen.blit(image, (144, 45))

# Función para dibujar el contenido de la pantalla alternativa
def record_screen():
    screen.fill(WHITE)
    
    # Dibujar los botones
    rect1 = pygame.Rect(270, 278, 180, 53)
    pygame.draw.rect(screen, GREEN, rect1)
    draw_text_centered("Grabar", font, WHITE, rect1)

rect1 = pygame.Rect(270, 278, 180, 53)
rect2 = pygame.Rect(270, 360, 180, 53)

running = True
running2 = False
while running:
    main_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if is_within_rect(mouse_pos, rect1):
                running = False
                running2 = True
            elif is_within_rect(mouse_pos, rect2):
                # Se hizo clic dentro de la segunda caja (rect2)
                print("Se hizo clic en la caja 2 (Reproducir)")

    pygame.display.update()

while running2:
    record_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running2 = False

    pygame.display.update()

# Finalizar Pygame
pygame.quit()