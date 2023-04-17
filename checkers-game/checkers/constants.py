import pygame

#dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

#colours
RED = (233, 100, 121)
BLACK = (77, 69, 93)
WHITE = (245, 233, 207)
BLUE = (125, 185, 182)
GREY = (0, 0, 0)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'),(50,50))