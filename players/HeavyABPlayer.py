"""
MiniMax Player with AlphaBeta pruning with heavy heuristic
"""
from players.AbstractPlayer import AbstractPlayer


# TODO: you can import more modules, if needed
import time
import utils
import numpy as np
from SearchAlgos import AlphaBeta , TimeOut
from copy import deepcopy


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.algo_to_search = AlphaBeta(self.utility, self.succ, None, self.goal)
    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.
        super().set_game_params(board)

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        # TODO: erase the following line and implement this function.
        move = self._iterative_minmax_algoritem(-1)
        self.turn += 1
        return move

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        rival_pos, rival_soldier, my_dead_pos = move

        if self.turn < 18:
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        else:
            rival_prev_pos = self.rival_pos[rival_soldier]
            self.board[rival_prev_pos] = 0
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        if int(my_dead_pos) != -1:
            self.board[my_dead_pos] = 0
            dead_soldier = int(np.where(self.my_pos == my_dead_pos)[0][0])
            self.my_pos[dead_soldier] = -2
        self.turn += 1


    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed
    def _iterative_minmax_algoritem(self, time_limit):
        """
        run minmax algo with deph + 1 in each iterative untill timeout
        """
        old_state = [self.board, 1, -1]
        current_deph = 3
        _, state , end_game = self.algo_to_search.search(old_state, current_deph, True, self.turn, -1)
        new_state = state
        return self._compere_move_to_board(new_state)

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, and perform_move functions used in AlphaBeta algorithm