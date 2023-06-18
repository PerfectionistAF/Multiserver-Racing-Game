import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Pygame Chat")

# Set up the font
font = pygame.font.SysFont(None, 25)

# Set up the chatbot's responses
responses = ["Hello!", "How can I help you?", "What's up?", "Nice to meet you!"]

# Start the chat loop
def chat():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Get the user's input
                    user_input = input_box.text
                    print(user_input)

                    # Reset the input box
                    input_box.text = ""
                    input_box.render()

                    # Choose a random response from the chatbot
                    chatbot_response = random.choice(responses)
                    print(chatbot_response)

                    # Render the chatbot's response
                    chatbot_render = font.render(chatbot_response, True, (255, 255, 255))
                    screen.blit(chatbot_render, (100, 100))
        # Update the display
        screen.fill((0, 0, 0))
        screen.blit(input_box.surface, (100, 500))
        screen.blit(chatbot_render, (100, 100))
        pygame.display.update()

# Define the input box class
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.font = font
        self.surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the input box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.surface.get_width()+10)
        self.rect.w = width

    def render(self):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.surface, (self.rect.x+5, self.rect.y+5))

# Set up the input box
input_box = InputBox(100, 550, 600, 30)

# Start the chat loop
chat()