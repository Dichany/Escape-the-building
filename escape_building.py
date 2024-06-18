import pygame
import time
from pygame.locals import *

# Initialization of pygame
pygame.init()

# Dimensions of the windows
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 698
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escape the Building")

# Loading images
background = pygame.image.load('building.JPG')
man = pygame.image.load('character.JPG')
man = pygame.transform.scale(man, (70, 70))  # resize of the character

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)
question_font = pygame.font.Font(None, 25)  # font size for the questions

# location of the character
x = SCREEN_WIDTH * 0.22
y = 10  

# Calcul de la distance de descente pour quatre descentes
DESCENT_DISTANCE = (SCREEN_HEIGHT - y - 60) // 4

target_y = y  # target position is the current position

# List of questions and answers
questions = [
    {"question": "integral of e^(-x²) between - and + infinity at 10^-2", "answer": "1.77"},
    {"question": "I am taller sitting than standing. Who am I?", "answer": "Dog"},
    {"question": "I keep raindrops spherical and allow insects to walk on water?", "answer": "Surface tension"},
    {"question": "What is the chemical symbol for water?", "answer": "H2O"}
]

# Index of the current question
current_question_index = 0

# Variables 
attempts = 2
start_time = time.time()
time_limit = 600  # 10 minutes in seconds for the whole game
answer = ""
game_over = False                                                   
win = False
man_moving_down = False  # Indicator to know if the character is moving down

def display_message(message, color, y_offset=0, align_right=False):
    """Affiche un message aligné à droite de l'écran ou centré."""
    text = font.render(message, True, color)
    if align_right:
        text_rect = text.get_rect(topright=(SCREEN_WIDTH - 40, SCREEN_HEIGHT // 2 + y_offset))
    else:
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

def display_question(message, color, y_offset=0):
    """Affiche une question à droite de l'écran."""
    text = question_font.render(message, True, color)
    text_rect = text.get_rect(topright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

def check_time():
    """Vérifie si le temps limite est écoulé."""
    current_time = time.time()
    return current_time - start_time >= time_limit

def move_man_down():
    """Déplace le personnage vers le bas jusqu'à la position cible."""
    global y, man_moving_down, target_y, game_over, win
    if y < target_y:
        y += 2  # move down the character of 2 pixels 
        if y >= target_y:
            y = target_y  # make sure the character stops at target_y
            man_moving_down = False
            if current_question_index >= len(questions):
                win = True  # The player answered correctly the last question and won
                game_over = True  # end of game after the last question

# Main loop of the game
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background, (0, 0))
    
    # display the character
    screen.blit(man, (x, y))
    
    # manage the events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_BACKSPACE:
                answer = answer[:-1]  # Delete the last character
            elif event.key == K_RETURN:
                if answer.lower() == questions[current_question_index]["answer"].lower():
                    # Correct answer
                    if current_question_index < len(questions) - 1:
                        man_moving_down = True
                        current_question_index += 1
                        target_y = y + DESCENT_DISTANCE  # Define the new target position
                        answer = ""
                        attempts = 2  # Reset the attempts for the next question
                    else:
                        man_moving_down = True
                        target_y = y + DESCENT_DISTANCE  # Move after the last question
                        current_question_index += 1  # Get out the list of questions to stop the game after the final move
                        answer = ""
                else:
                    # Wrong answer
                    attempts -= 1
                    if attempts == 0:
                        game_over = True  # stop the game if the attempts are done
                    else:
                        answer = ""
            else:
                answer += event.unicode  

    # Check the elapsed time only if the game is not over
    
    if not game_over:
        if check_time():
            game_over = True

    # Display the current question only if we haven't exceeded the number of questions
    if current_question_index < len(questions):
        display_question(questions[current_question_index]["question"], GREEN, -250)
    
    # display the answer given by the player
    display_message(answer, BLUE, -150, align_right=True)
    
    # display the remaining attempts 
    display_message(f"Attempts remaining: {attempts}", RED, -100, align_right=True)
    
    # display the time remaining if only the game isn't over 
    if not game_over:
        time_remaining = max(0, time_limit - int(time.time() - start_time))
        display_message(f"Time remaining: {time_remaining}s", RED, -50, align_right=True)

    if game_over:
        if win:
            display_message("Congratulations!", GREEN, 50, align_right=True)
        else:
            display_message("Game over. You lose!", RED, 50, align_right=True)
    
    # Move the character if the player answered correctly
    if man_moving_down:
        move_man_down()

    pygame.display.flip()
    
    # Limit the framerate
    pygame.time.Clock().tick(30)

pygame.quit()
