import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, BLACK, BLUE, WHITE
from checkers.board import Board
from checkers.game import Game
from minimax.algorithm import minimax
FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHECKERS')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

pygame.font.init()                

#drawing background
background = pygame.Surface(WIN.get_size())
background.fill(BLUE)
WIN.blit(background, (0, 0))

#drawing title
font1 = pygame.font.SysFont("jokerman", 150)
title_text = font1.render("Checkers", True, BLACK)
title_pos = ((WIDTH - title_text.get_width()) / 2, 200)
WIN.blit(title_text, title_pos)

# Draw buttons
button_width = 400
button_height = 100
button_gap = 50

button_font = pygame.font.SysFont("segoeprint", 50)

# Play button
play_button = pygame.Surface((button_width, button_height))
play_button.fill(RED)
play_button_pos = ((WIDTH - button_width) / 2, 450)
WIN.blit(play_button, play_button_pos)

play_text = button_font.render("Play Game", True, WHITE)
play_text_pos = ((button_width - play_text.get_width()) / 2, (button_height - play_text.get_height()) / 2)
play_button.blit(play_text, play_text_pos)
WIN.blit(play_button, play_button_pos)

pygame.display.flip()


# Define a function to display the game over message
def display_game_over(winner):
    if winner == RED:
        background = pygame.image.load('RedWon.png') 
        background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 
        WIN.blit(background,(0,0)) 
        
    else:
        background = pygame.image.load('WhiteWon.png') 
        background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 
        WIN.blit(background,(0,0)) 
        
    pygame.display.flip()    
    
         
def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    flag = True
    c = 0 
    while(run):
        clock.tick(FPS)
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(),3, WHITE, game)
            game.ai_move(new_board)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            pos = pygame.mouse.get_pos()
            row, col = get_row_col_from_mouse(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pos
                left, right = play_button.get_size()
                if x <= left and y >= right:
                    game.update()
                    flag = False

                game.select(row,col)  
            if flag == False:
                game.update()
        
        if game.winner() != None:
            display_game_over(game.winner())
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

main()