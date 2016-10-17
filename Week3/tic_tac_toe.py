"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 10         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board,player):
    """
    This function takes a current board and the next player to move.
    The function should play a game starting with the given player by making random moves, alternating between players.
    The function should return when the game is over.
    The modified board will contain the state of the game,
    so the function does not return anything. In other words,
    the function should modify the board input.
    """
    while(board.check_win() == None):
        empty = board.get_empty_squares()
        next_move = random.choice(empty)
        board.move(next_move[0],next_move[1],player)
        player = provided.switch_player(player)



def mc_update_scores(scores,board,player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions as the Tic-Tac-Toe board,
    a board from a completed game, and which player the machine player is.
    The function should score the completed board and update the scores grid.
    As the function updates the scores grid directly, it does not return anything,
    """
    winner = board.check_win()
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if winner == provided.DRAW:
                scores[row][col] +=0
            elif winner == board.square(row,col) and winner == player:
                scores[row][col] += SCORE_CURRENT
            elif winner == board.square(row,col) and winner != player:
                scores[row][col] += SCORE_OTHER
            elif winner != board.square(row,col) and winner == player and board.square(row,col) != provided.EMPTY:
                scores[row][col] -=SCORE_OTHER
            elif winner != board.square(row,col) and winner != player and board.square(row,col) != provided.EMPTY:
                scores[row][col] -=SCORE_CURRENT
            else:
                scores[row][col] +=0



def get_best_move(board,scores):
    """
    This function takes a current board and a grid of scores.
    The function should find all of the empty squares with the maximum score
    and randomly return one of them as a (row,column) tuple. It is an error to call this function with a board that has no empty squares
    (there is no possible next move), so your function may do whatever it wants in that case.
    The case where the board is full will not be tested.
    """
    if (len(board.get_empty_squares())!=0):
        empty = board.get_empty_squares()
        max_score = max([scores[coord[0]][coord[1]] for coord in empty])
        max_coord = []
        for dummy_p in empty:
            if scores[dummy_p[0]][dummy_p[1]] == max_score:
                max_coord.append(dummy_p)
        random_pick = random.choice(max_coord)
        return random_pick



def mc_move(board,player,trails):
    """
    This function takes a current board, which player the machine player is,and the number of trials to run.
    The function should use the Monte Carlo simulation described above to return a move
    for the machine player in the form of a (row,column) tuple. Be sure to use the other functions you have written!

    """
    score_board = [ [0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]
    for dummy_i in range(trails):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(score_board, trial_board, player)

    row, col = get_best_move(board, score_board)

    return row, col



# Test game with the console or the GUI.  Uncomment whichever
# you prefer.  Both should be commented out when you submit
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)
# poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
