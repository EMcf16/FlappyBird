import pygame, sys
from random import choice


class Bird(pygame.sprite.Sprite):
    """Overall class to manage player attributes and resources."""

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "graphics/yellowbird-midflap.png"
        ).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)
        self.rect = self.image.get_rect(midbottom=(300, 300))
        self.gravity = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and cooldown_tracker == 0:
            self.gravity = -6

    def apply_gravity(self):
        self.gravity += 0.3
        self.rect.y += self.gravity

    def floor_collision(self):
        if bird.rect.y >= 500:
            bird.rect.y = 300
            return False
        else:
            return True

    def update(self):
        self.apply_gravity()
        self.player_input()


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.image = pygame.image.load("graphics/pipe.png")
        self.image = pygame.transform.rotozoom(self.image, 180, 1.5)
        self.rect = self.image.get_rect(midbottom=(1000, height))

    def move_pipes(self):
        self.rect.x -= 4

    def update(self):
        self.move_pipes()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


class BottomPipe(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.image = pygame.image.load("graphics/pipe.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 1.5)
        self.rect = self.image.get_rect(midtop=(1000, height + 180))

    def move_pipes(self):
        self.rect.x -= 4

    def update(self):
        self.move_pipes()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def draw_floor():
    screen.blit(floor, (floor_x_pos, 500))
    screen.blit(floor, (floor_x_pos + 795, 500))


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
game_active = False
cooldown_tracker = 0
pipe_height = [50, 100, 150, 200, 250]

background = pygame.image.load("graphics/background.png").convert()
floor = pygame.image.load("graphics/floor.PNG").convert()
floor = pygame.transform.scale(floor, (800, 200))
floor_x_pos = 0

start_message = pygame.image.load("graphics/message.png").convert_alpha()
start_message = pygame.transform.rotozoom(start_message, 0, 1.5)

bird = Bird()
pipe_group = pygame.sprite.Group()

# Timer
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_active = True
        if event.type == pipe_timer and game_active:
            rand_height = choice(pipe_height)
            pipe_group.add(TopPipe(rand_height), BottomPipe(rand_height))

    screen.blit(background, (0, 0))
    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -800:
        floor_x_pos = 0

    if game_active:
        pipe_group.draw(screen)
        pipe_group.update()
        draw_floor()
        bird.draw()
        bird.update()
        game_active = bird.floor_collision()
    else:
        screen.blit(start_message, (250, 80))
        pipe_group.empty()

    pygame.display.update()
    clock.tick(120)
