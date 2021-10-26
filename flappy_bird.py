import pygame, sys
from random import choice


class Bird(pygame.sprite.Sprite):
    """Overall class to manage player attributes and resources."""

    def __init__(self):
        super().__init__()
        self.upflap = pygame.image.load(
            "graphics/yellowbird-upflap.png"
        ).convert_alpha()
        self.upflap = pygame.transform.rotozoom(self.upflap, 0, 1.5)
        self.midflap = pygame.image.load(
            "graphics/yellowbird-midflap.png"
        ).convert_alpha()
        self.midflap = pygame.transform.rotozoom(self.midflap, 0, 1.5)
        self.downflap = pygame.image.load(
            "graphics/yellowbird-downflap.png"
        ).convert_alpha()
        self.downflap = pygame.transform.rotozoom(self.downflap, 0, 1.5)

        self.gravity = 0
        self.bird_index = 0
        self.bird_animation = [self.upflap, self.midflap, self.downflap]
        self.image = self.bird_animation[self.bird_index]
        self.rect = self.image.get_rect(midbottom=(300, 300))

    def animation(self):
        self.bird_index += 0.1
        if self.bird_index >= len(self.bird_animation):
            self.bird_index = 0
        self.image = self.bird_animation[int(self.bird_index)]

    def draw(self):
        rotated_bird = pygame.transform.rotozoom(self.image, -self.gravity * 3, 1)
        screen.blit(rotated_bird, self.rect)

    def player_input(self):
        keys = pygame.key.get_pressed()
        mouse_click = pygame.mouse.get_pressed()[0]
        if mouse_click:
            self.gravity = -6
        if keys[pygame.K_SPACE] and cooldown_tracker == 0:
            self.gravity = -6

    def apply_gravity(self):
        self.gravity += 0.25
        self.rect.y += self.gravity

    def update(self):
        self.animation()
        self.apply_gravity()
        self.player_input()


class TopPipe(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.image = pygame.image.load("graphics/pipe.png")
        self.image = pygame.transform.rotozoom(self.image, 180, 1.5)
        self.rect = self.image.get_rect(midbottom=(1000, height))

    def move_pipes(self):
        self.rect.x -= 3

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
        self.rect.x -= 3

    def update(self):
        self.move_pipes()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def draw_floor():
    screen.blit(floor, (floor_x_pos, 500))
    screen.blit(floor, (floor_x_pos + 795, 500))


def sprite_collision():
    if pygame.sprite.spritecollide(bird, pipe_group, False):
        return False
    else:
        return True


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
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        game_active = sprite_collision()  # Checking for pipe collision
        if bird.rect.y >= 500:  # Checking for floor collision
            bird.rect.y = 300
            game_active = False
    else:
        screen.blit(start_message, (250, 80))
        bird.rect.y = 300
        pipe_group.empty()

    pygame.display.update()
    clock.tick(120)
