import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Flappy Bird')

background = pygame.image.load('graphics/background.png').convert()
floor = pygame.image.load('graphics/floor.PNG').convert()
floor = pygame.transform.scale(floor,(800,200))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background, (0,0))
    screen.blit(floor, (0,450))
    pygame.display.update()
