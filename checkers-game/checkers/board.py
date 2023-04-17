import pygame
# relative import
from .constants import RED, WHITE, BLACK, GREY, ROWS, COLS, SQUARE_SIZE, WIDTH, HEIGHT
from .piece import Piece
from copy import deepcopy
# state of game


class Board:
    def __init__(self) -> None:
        self.board = []  # 8 X 8 matrix
        self.red_left = 12
        self.white_left = 12
        self.red_kings = 0
        self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):  # to start in the alternate columns
                pygame.draw.rect(win, GREY, (row*SQUARE_SIZE,
                                 col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.rect(win, RED, ((
                    row*SQUARE_SIZE) - 2, (col*SQUARE_SIZE) - 2, SQUARE_SIZE - 2, SQUARE_SIZE - 2))

    def get_all_moves(board, color, game):
        moves = []  # [[board1, piece1], [board2, piece2]]
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                # we make a copy of old board to not make changes
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                # makes move on temporary board and put it here
                new_board = temp_board.simulate_board(
                    temp_piece, move, game, skip)
                moves.append(new_board)

        return moves

    def simulate_board(self, piece, move, game, skip):
        self.move(piece, move[0], move[1])
        if skip:
            self.remove(skip)
        return self

    # AI: The score for each move:
    def evaluate(self, game):

        return (self.white_left - self.red_left)*2 + (0.5*self.white_kings - 0.5*self.red_kings)

    # AI: to get all the pieces of that colour on the board
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        # swap the positions from original to new
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:  # it happens only after move so won't affect original position
            if piece.color == WHITE and piece.king == False:
                self.white_kings += 1
                piece.make_king()
            elif piece.color == RED and piece.king == False:
                self.red_kings += 1
                piece.make_king()

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # where to draw to pieces i.e first even columns then odd columns then even....
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        moves = {}
        # (4, 5) = available space = key
        # (4,5) : [(3,4)] we surpass (3,4) to go to move (4,5)
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            # we check up (row - 1), how far up (max(row-3)#not further than two pieces away,-1),-1: move up, left = what to substract
            moves.update(self._traverse_left(
                row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(
                row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(
                row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(
                row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:  # found empty square
                if skipped and not last:  # if next square after jump is blank, we don't move forward
                    break
                elif skipped:  # found valid move and skipped, are double jumping, we combine last checker we jumped and this time's jump
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last  # if move is possible, we add it

                if last:  # we skipped over and preparing to double jump
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    # do everything again to see of we can double jump or not
                    moves.update(self._traverse_left(
                        r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, left + 1, skipped=last))
                break

            elif current.color == color:  # if we find our color then we can't move there
                break

            else:
                # we can move over the it assuming next square is empty
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:  # found empty square
                if skipped and not last:  # if next square after jump is blank, we don't move forward
                    break
                elif skipped:  # found valid move and skipped, are double jumping, we combine last checker we jumped and this time's jump
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last  # if move is possible, we add it

                if last:  # we skipped over and preparing to double jump
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    # do everything again to see of we can doubble jump or not
                    moves.update(self._traverse_left(
                        r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(
                        r + step, row, step, color, right + 1, skipped=last))
                break

            elif current.color == color:  # if we find our color then we can't move there
                break

            else:
                # we can move over the it assuming next square is empty
                last = [current]

            right += 1

        return moves

    # start, stop, step = where to go up or down or top left or bottom left diagonal
    # skipped = have we skipped any pieces?? we can then only move to squares where we skip another piece
    # left = where we starting in terms of column

    # valid moves:
    # we can move on diagonals
    # king can move backward also
    # sometimes we can double jump

    # algo:
    # first we check colour to get direction say red
    # check the diagonals first say we check the first left diagonal square:
    # if there is red piece, we can't move there
    # if piece is empty, we can move there
    # if it has opposite colour piece we must move on that diagonal to see if we can go forward there
    # do the same on right side

    # for double jump
    # we see if we can move above any other opponent piece
