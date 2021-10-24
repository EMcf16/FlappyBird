import pygame
import sys

class Bird(pygame.sprite.Sprite):
    '''Overall class to manage player attributes and resources.'''
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/yellowbird-midflap.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image,0,1.5)
        self.rect = self.image.get_rect(midbottom = (300,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -8
    
    def apply_gravity(self):
        self.gravity += 0.3
        self.rect.y += self.gravity

    def update(self):
        self.apply_gravity()
        self.player_input()

def draw_floor():
    screen.blit(floor, (floor_x_pos,500))
    screen.blit(floor, (floor_x_pos+795,500))

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

background = pygame.image.load('graphics/background.png').convert()
floor = pygame.image.load('graphics/floor.PNG').convert()
floor = pygame.transform.scale(floor,(800,200))
floor_x_pos = 0

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(background, (0,0))
    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -800: floor_x_pos = 0
    bird.draw(screen)
    bird.update()

    pygame.display.update()
    clock.tick(120)
