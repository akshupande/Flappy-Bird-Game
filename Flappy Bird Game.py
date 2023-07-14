import pygame
import random

# Set up the game window
pygame.init()
win_width = 500
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Flappy Bird")

# Load game assets
bg_img = pygame.image.load("backgrd.jpeg").convert()
bird_img = pygame.image.load("bird.png").convert()
pipe_img = pygame.image.load("pipe.jpeg").convert()
flap_sound = pygame.mixer.Sound("point.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")

# Define game objects
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 200
        self.speed = 5

    def update(self):
        self.rect.y += self.speed

    def jump(self):
        self.speed = -5
        flap_sound.play()

class Pipe(pygame.sprite.Sprite):
    def __init__(self, height):
        super().__init__()
        self.image = pipe_img
        self.rect = self.image.get_rect()
        self.rect.x = win_width
        self.rect.y = height

    def update(self):
        self.rect.x -= 2

# Set up game variables
bird = Bird()
pipes = pygame.sprite.Group()
score = 0
font = pygame.font.Font(None, 36)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update game objects
    bird.update()
    pipes.update()

    # Check for collisions
    if pygame.sprite.spritecollide(bird, pipes, False):
        hit_sound.play()
        pygame.time.delay(1000)
        pygame.quit()
        quit()

    # Check for score
    for pipe in pipes:
        if pipe.rect.right < bird.rect.left and not pipe.scored:
            pipe.scored = True
            score += 1

    # Generate new pipes
    if len(pipes) < 5:
        pipe_height = random.randint(150, 400)
        top_pipe = Pipe(pipe_height - 640)
        bottom_pipe = Pipe(pipe_height + 200)
        pipes.add(top_pipe, bottom_pipe)

    # Draw game objects
    win.blit(bg_img, (0, 0))
    pipes.draw(win)
    win.blit(bird.image, bird.rect)
    score_text = font.render(str(score), True, (255, 255, 255))
    win.blit(score_text, (win_width - 50, 10))
    pygame.display.update()

    # Remove off-screen pipes
    for pipe in pipes:
        if pipe.rect.right < 0:
            pipes.remove(pipe)
