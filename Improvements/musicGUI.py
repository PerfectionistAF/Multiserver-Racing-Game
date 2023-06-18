import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Load the music file
pygame.mixer.music.load('bg_music.mp3')

# Load the sound effect files
eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over_sound.wav')

# Set up the game window
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Define the Snake class
class Snake:
    def __init__(self):
        self.head = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self, direction):
        if direction == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        elif direction == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        elif direction == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, food_position):
        if self.direction == "RIGHT":
            self.head[0] += 10
        elif self.direction == "LEFT":
            self.head[0] -= 10
        elif self.direction == "UP":
            self.head[1] -= 10
        elif self.direction == "DOWN":
            self.head[1] += 10

        self.body.insert(0, list(self.head))

        if self.head == food_position:
            eat_sound.play()
            return 1

        self.body.pop()
        return 0

    def check_collision(self):
        if self.head[0] >= width or self.head[0] < 0 or self.head[1] >= height or self.head[1] < 0:
            return 1

        for block in self.body[1:]:
            if self.head == block:
                return 1

        return 0

    def get_head_position(self):
        return self.head

    def get_body_position(self):
        return self.body

# Define the Food class
class Food:
    def __init__(self):
        self.position = [random.randrange(1, (width//10))*10, random.randrange(1, (height//10))*10]
        self.color = (223, 163, 49)

    def randomize_position(self):
        self.position = [random.randrange(1, (width//10))*10, random.randrange(1, (height//10))*10]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], 10, 10))

# Create the Snake and Food objects
snake = Snake()
food = Food()

# Start playing the music
pygame.mixer.music.play(loops=-1)

# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.change_to = "RIGHT"
            elif event.key == pygame.K_LEFT:
                snake.change_to = "LEFT"
            elif event.key == pygame.K_UP:
                snake.change_to = "UP"
            elif event.key == pygame.K_DOWN:
                snake.change_to = "DOWN"
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Update the game state
    if snake.change_to != snake.direction:
        snake.change_direction(snake.change_to)

    eaten = snake.move(food.position)

    if eaten:
        food.randomize_position()

    if snake.check_collision():
        game_over_sound.play()
        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

    # Draw the game objects
    screen.fill((0, 0, 0))
    for block in snake.get_body_position():
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(block[0], block[1], 10, 10))
    food.draw(screen)

    # Update the display
    pygame.display.update()

# Stop the music when the game is over
pygame.mixer.music.stop()