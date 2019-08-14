import pygame

# Load audio
pygame.mixer.init()
pygame.mixer.music.load("dialtone.mp3")

pygame.mixer.music.play(-1,0.0)

while True:
    try:
        pass
    except KeyboardInterrupt:
        break