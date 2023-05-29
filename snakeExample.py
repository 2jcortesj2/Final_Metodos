import pygame
import random
import threading
from model import Sonido

# Colores con los que vamos a trabajar
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Inicializar pygame
pygame.init()

# Definir el tammaño de la  pantalla
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20

# Velocidad de la serpiente
SNAKE_SPEED = 5

# Crear ventana de juego
screen = pygame.display.set_mode( [SCREEN_WIDTH, SCREEN_HEIGHT] )
pygame.display.set_caption('Snake Game') # vamos a  definir el nombre de la ventana
clock = pygame.time.Clock() # Reloj

# Definir fuente utilizada
font = pygame.font.SysFont( "Times New Roman", 25 )

# creamos la clase snake
class Snake:
    def __init__(self):
        self.positions = [(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)]
        self.direction = random.choice(["L", "R", "U", "D"])   
    def move(self):
        x, y = self.positions[0]
        if self.direction[0] == "U":
            y -= SNAKE_SPEED
        elif self.direction[0] == "D":
            y += SNAKE_SPEED
        elif self.direction[0] == "L":
            x -= SNAKE_SPEED
        elif self.direction[0] == "R":
            x += SNAKE_SPEED
        self.positions.insert(0, (x, y))
        self.positions.pop() # elimina el ultimo elemento de la lista dejando asi siempre la posicion en la que se encuentra  
    def change_direction(self, direction):
        if direction == "U" and self.direction != "D":
            self.direction = "U"
        elif direction == "D" and self.direction != "U":
            self.direction = "D"
        elif direction == "L" and self.direction != "R":
            self.direction = "L"    
        elif direction == "R" and self.direction != "L":
            self.direction = "R"
    def add_segment(self):
        self.positions.append(self.positions[-1])
    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(surface, GREEN, (position[0], position[1], CELL_SIZE, CELL_SIZE))

# Clase para la manzana
class Apple:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    def randomize_position(self):
        x = random.randint(0, SCREEN_WIDTH/CELL_SIZE - 1) * CELL_SIZE
        y = random.randint(0, SCREEN_HEIGHT/CELL_SIZE - 1) * CELL_SIZE
        self.position = (x, y)
    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE - 1/2, CELL_SIZE - 1/2))

def draw_text(text, font, surface, x, y): # Creamos este para poder dibujar texto 
    text_object = font.render(text, True, WHITE)  # el render es especifico de pygame para añadir texto en las pantallas
    text_rect = text_object.get_rect() 
    text_rect.center = (x, y)
    surface.blit(text_object, text_rect)


sonido = Sonido()
snake = Snake()
apple = Apple()

game_over = False
run = True
score = 0
i=0

# Crear el bucle
while run == True:
    # Controlar eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
        elif event.type == pygame.KEYDOWN: # que ha presionado una tecla
            if event.key == pygame.K_UP: # quiero que cambie la direccion hacia arriba
                snake.change_direction("U")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("D") # para cambiar la posicion hacia abajo
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("R") # para cambiar la posicion hacia la derecha
            elif event.key == pygame.K_LEFT:
                snake.change_direction("L") # para cambiar la posicion hacia la izquierda
            elif event.key == pygame.K_r and game_over == True:
                # Reiniciar juego
                snake = Snake()
                apple = Apple()
                score = 0
                game_over = False

    if game_over == False:
        # move the snake
        snake.move()

        if snake.positions[0][0] < 0 or snake.positions[0][0] > (SCREEN_WIDTH - CELL_SIZE) or snake.positions[0][1] < 0 or snake.positions[0][1] > (SCREEN_HEIGHT - CELL_SIZE):  
            game_over = True
        for position in snake.positions[1:]:
            if snake.positions[0] == position:
                game_over = True
    
    # Comprobar si la serpiente come una manzana
    if snake.positions[0] == apple.position:
        apple.randomize_position()
        snake.add_segment()
        score += 1

    # Dibujos de la pantalla        
    screen.fill(BLACK)
    draw_text("Score: {}".format(score), font, screen, SCREEN_WIDTH/2, 10)
    snake.draw(screen)
    apple.draw(screen)

    if game_over == True: # No entendi muy bien el por que tiene que ir despues de los dibujos de pantalla
        draw_text("GAME OVER", font, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        draw_text("Presiona R para continuar", font, screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)
    
    # Actualizar pantalla 
    pygame.display.update()
    clock.tick(10) # velocidad de los fps
    sonido.grabarAudio(r"Records\Temp\a.wav", 1)

pygame.quit()