# Tetris in PyGame
import pygame
import random
import sys
import os
from variables import *
from classes import Shape
from classes import Tetris

pygame.init()
pygame.mixer.init()
# Load and set volume for background music and sound effects
game_music = os.path.join('Assets', 'Tetris Sound.mp3')
intro_music = os.path.join('Assets', 'intro.mp3')
game_over_music =  os.path.join('Assets', 'game-over.wav')
clear_path = os.path.join('Assets', 'clear-line.wav')
clear_sound = pygame.mixer.Sound(clear_path)
clear_sound.set_volume(0.5)
game_over_sound = pygame.mixer.Sound(game_over_music)

# Set the window title
pygame.display.set_caption("Tetris Game")

# Existing game code follows...
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

def draw_countdown():
    # Load countdown background image
    countdown_bg = pygame.image.load(os.path.join('Assets', 'cd_image.jpg'))
    countdown_bg = pygame.transform.scale(countdown_bg, (WIDTH, HEIGHT))
    
    countdown_font = pygame.font.Font(font_path, 60)  # Font for countdown numbers

    # Countdown loop
    for count in ["3", "2", "1", "GO!"]:
        SCREEN.blit(countdown_bg, (0, 0))  # Display background
        countdown_text = countdown_font.render(count, True, WHITE)
        text_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        SCREEN.blit(countdown_text, text_rect)
        
        pygame.display.update()
        pygame.time.delay(1000)  # Wait 1 second before showing the next count

def draw_start_screen():
    #play start music
    pygame.mixer.music.load(intro_music)
    pygame.mixer.music.play(-1)
    
    # Load background image
    bg_image = pygame.image.load(os.path.join('Assets', 'BG.png'))
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))  # Scale image to fit screen size
    SCREEN.blit(bg_image, (0, 0))  # Draw the background image to cover the entire screen

     # Load font for the title and buttons
    title_font = pygame.font.Font(font_path, 35)  # Set a larger font size for the title
    button_font = pygame.font.Font(font_path, 20)

    # Render the title text
    title_text = title_font.render("Tetris\n Game", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    SCREEN.blit(title_text, title_rect)

    # Play Button
    play_text = button_font.render("Play", True, WHITE)
    play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(play_text, play_rect)
    
    # Quit Button
    quit_text = button_font.render("Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
    SCREEN.blit(quit_text, quit_rect)

    pygame.display.update()  # Update display once, outside the event loop

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    pygame.mixer.music.load(game_music) # Load game music here, only when starting
                    pygame.mixer.music.play(-1)
                    clear_sound.play()
                    draw_countdown()  # Start countdown after Play button is clicked
                    waiting = False  # Exit the loop immediately
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def save_high_score(score):
    try:
        with open("high_scores.txt", "a") as file:
            file.write(f"{score}\n")
    except Exception as e:
        print(f"Error saving high score: {e}")

def load_high_scores():
    scores = []
    try:
        with open("high_scores.txt", "r") as file:
            scores = file.readlines()
        scores = [int(score.strip()) for score in scores]
    except Exception as e:
        print(f"Error loading high scores: {e}")
    return scores

def display_scores(tetris, high_score):
    # Render and display the score and high score
    score_text = font.render(f"Score: {tetris.score}", True, WHITE)
    high_score_text = font2.render(f"High Score: {high_score}", True, WHITE)
    
    # Blit text to the screen
    SCREEN.blit(score_text, (250 - score_text.get_width() // 2, HEIGHT - 110))
    SCREEN.blit(high_score_text, (WIDTH - 10 - high_score_text.get_width(), HEIGHT - 60))

def clear_full_rows(tetris):
    cleared_rows = 0
    for i in range(ROWS):
        if tetris.grid[i].count(0) == 0:  # Row is full
            cleared_rows += 1
            for j in range(i, 0, -1):
                tetris.grid[j] = tetris.grid[j-1][:] # Shift rows down
            tetris.grid[0] = [0 for _ in range(COLS)] # New empty row
  
    # Add score for cleared rows
    if cleared_rows == 1:
        tetris.score += SINGLE_CLEAR_SCORE
    elif cleared_rows == 2:
        tetris.score += DOUBLE_CLEAR_SCORE
    elif cleared_rows == 3:
        tetris.score += TRIPLE_CLEAR_SCORE
    elif cleared_rows == 4:
        tetris.score += TETRIS_CLEAR_SCORE

if __name__ == "__main__":
    draw_start_screen()
# Main Game Loop
def main():
    tetris = Tetris(ROWS, COLS)
    clock = pygame.time.Clock()
    counter = 0
    move = True
    space_pressed = False
    run = True

    high_scores = load_high_scores()
    high_score = max(high_scores, default=0)

    while run:
        SCREEN.blit(bg_image, (0, 0))  # Draw background image
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            # Event Loop
            keys = pygame.key.get_pressed()
            if not tetris.end:
                if keys[pygame.K_LEFT]:
                    tetris.left()
                elif keys[pygame.K_RIGHT]:
                    tetris.right()
                elif keys[pygame.K_DOWN]:
                    tetris.move_down()
                elif keys[pygame.K_UP]:
                    tetris.rotate()
                elif keys[pygame.K_SPACE]:
                    space_pressed = True
            if keys[pygame.K_r]:
                tetris.__init__(ROWS, COLS)
                pygame.mixer.music.play()
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                run = False 
                
        # Allows block to fall at constant rate
        counter += 1
        if counter >= 15000:
            counter = 0
                
        if move:
            if counter % (FPS //(tetris.level*1)) == 0:
                if not tetris.end:
                    if space_pressed:
                        tetris.freefall()
                        space_pressed = False
                    else:
                        tetris.move_down()
                        
        tetris.make_grid()
        clear_full_rows(tetris)
        
        # Keep Fallen Shapes on Screen
        for x in range(ROWS):
            for y in range(COLS):
                if tetris.grid[x][y] > 0:
                    value = tetris.grid[x][y]
                    image = ASSETS[value]
                    SCREEN.blit(image, (y*CELL, x*CELL))
                    pygame.draw.rect(SCREEN, WHITE, (y*CELL, x*CELL, CELL, CELL), 1)
                    
        # Show Shape on Game Screen
        if tetris.figure:
            for i in range(4):
                for j in range(4):
                    if (i *4 + j) in tetris.figure.image():
                        shape = ASSETS[tetris.figure.color]
                        x = CELL * (tetris.figure.x + j)
                        y = CELL * (tetris.figure.y + i)
                        SCREEN.blit(shape, (x,y))
                        pygame.draw.rect(SCREEN, WHITE, (x,y,CELL,CELL),1)
                        
        # Control Panel
        if tetris.next:
            for i in range(4):
                for j in range(4):
                    if (i *4 + j) in tetris.next.image():
                        image = ASSETS[tetris.next.color]
                        x = CELL * (tetris.next.x + j -4)
                        y = HEIGHT -100 + CELL * (tetris.next.y +i)
                        SCREEN.blit(image,(x,y))
        
        if tetris.end:
            tetris.end_game()
            save_high_score(tetris.score)
            high_score = max(high_score, tetris.score)

        score_text = font.render(f"{tetris.score}", True, WHITE)
        level_text = font2.render(f"Level: {tetris.level}", True, WHITE)
        high_score_text = font2.render(f"High Score: {high_score}", True, WHITE)

        SCREEN.blit(score_text, (250 - score_text.get_width() // 2, HEIGHT - 110))
        SCREEN.blit(level_text, (WIDTH - 10 - level_text.get_width(), HEIGHT - 30))
        SCREEN.blit(high_score_text, (WIDTH - 10 - high_score_text.get_width(), HEIGHT - 60))

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()