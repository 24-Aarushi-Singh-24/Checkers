import pygame

from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN

class Piece:
    
    PADDING = 17
    OUTLINE = 3
    def __init__(self, row, col, color) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.king = False
                    
        self.x = 0
        self.y = 0
        self.cal_pos()
        
    def cal_pos(self): #calculate x and y position
        self.x = (SQUARE_SIZE * self.col) + (SQUARE_SIZE // 2) #to be in the middle of square
        self.y = (SQUARE_SIZE * self.row) + (SQUARE_SIZE // 2)
        
    def make_king(self):
        self.king = True
    
    def draw(self, win):
        radius = (SQUARE_SIZE // 2) - self.PADDING
        pygame.draw.circle(win, GREY, (self.x,self.y), radius + self.OUTLINE) #border for the circle
        pygame.draw.circle(win, self.color, (self.x,self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - (CROWN.get_height() // 2)))
    
    def move(self, row, col):
        self.row = row
        self.col = col 
        self.cal_pos()
    
    def __repr__(self) -> str: #for debugging: shows internal representation of the object
        return str(self.color)