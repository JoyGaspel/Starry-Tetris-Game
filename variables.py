import pygame
import os
pygame.init()

WIDTH = 300
HEIGHT = 500
FPS = 60
CELL = 20
ROWS = (HEIGHT - 120) // CELL
COLS = WIDTH // CELL

SINGLE_CLEAR_SCORE = 100
DOUBLE_CLEAR_SCORE = 300
TRIPLE_CLEAR_SCORE = 500
TETRIS_CLEAR_SCORE = 800

# Load background image
bg_image = pygame.image.load(os.path.join('Assets', 'BG1.png'))
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

BLACK = (0,0,0)
WHITE = (255, 255, 255)
BG_COLOR = (0, 0, 55)
GRID = (0, 0, 76)
WIN = (50, 230, 50)
LOSE = (55, 118, 171)

# Load custom font
font_path = os.path.join('Assets', 'gamefont.ttf')
font = pygame.font.Font(font_path, 45)
font2 = pygame.font.Font(font_path, 10)
font3 = pygame.font.Font(font_path, 40)

ASSETS ={
    1: pygame.image.load("Assets/1.png"),
    2: pygame.image.load("Assets/2.png"),
    3: pygame.image.load("Assets/3.png"),
    4: pygame.image.load("Assets/4.png"),
}