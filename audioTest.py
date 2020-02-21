import pygame

pygame.mixer.init()
pygame.mixer.music.load("dial.mp3")
pygame.mixer.music.set_volume(10)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue

print("done")