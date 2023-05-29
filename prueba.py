import pygame
import sounddevice as sd
import numpy as np
import time

# Configuración de pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Configuración de sounddevice
duration = 1.0  # Duración de cada grabación en segundos
sample_rate = 44100  # Tasa de muestreo del audio

def record_audio(dt):
    frames = int(duration * sample_rate)
    audio = sd.rec(frames, samplerate=sample_rate, channels=2)
    sd.wait()  # Esperar a que termine la grabación
    filename = f"audio_{int(time.time())}.wav"  # Generar un nombre de archivo único
    sd.write(filename, audio, sample_rate)  # Guardar el archivo de audio

# Bucle principal del juego
running = True
while running:
    dt = clock.tick(30) / 1000.0  # Calcular el tiempo transcurrido desde el último fotograma en segundos

    # Lógica del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar en la pantalla
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Grabar audio cada segundo
    record_audio(dt)

# Salir del juego
pygame.quit()