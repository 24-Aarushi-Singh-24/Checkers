import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board


class Game:
    def __init__(self, win) -> None: #for playing multiple games
        self._init()
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_move)
        pygame.display.update()
        
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_move = {}
        
    def winner(self):
        return self.board.winner()
        
    def reset(self):
        self._init()
        
    def select(self, row, col):
        if self.selected:
            result = self._move(row,col) #trying to move piece to a certain square
            if not result: #if the move is invalid, we reset the selection and recall the select function again
                self.selected = None
                self.select(row,col)
             
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_move = self.board.get_valid_moves(piece)
            return True
        
        return False
        
    def _move(self,row,col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row,col) in self.valid_move:
            self.board.move(self.selected , row, col)
            skipped = self.valid_move[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win,BLUE,(col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
            c = 1
    
    
    def change_turn(self):
        self.valid_move = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
            
    def get_board(self):
        return self.board
    
    def ai_move(self, board): #gives new board after that move
        self.board = board
        self.change_turn()
        
            
    
    