from copy import deepcopy #copy reference(shallow copy) + object itself
import pygame

RED = (233, 100, 121)
WHITE = (245, 233, 207)

# position = board, depth = how deep do we check moves , max_player = true : we are trying to maximise
def minimax(position, depth, max_player, game): 
    if depth == 0 or position.winner() != None:
        return position.evaluate(game), position # best move and which position to moe
    if max_player: #for maximising
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game): #loop through all moves
            evaluation = minimax(move, depth - 1, False, game)[0] #evaluate
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
                
        return maxEval, best_move
    else: #for minimising
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
                
        return minEval, best_move
        
    
   
def get_all_moves(board, color, game):
    moves = [] # [[board1, piece1], [board2, piece2]]
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board) #we make a copy of old board to not make changes
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_board(temp_piece, move, temp_board, game, skip) #makes move on temporary board and put it here
            moves.append(new_board)
            
    return moves
            
            
def simulate_board(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board
    