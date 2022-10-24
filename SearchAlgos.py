"""Search Algos: MiniMax, AlphaBeta
"""
# TODO: you can import more modules, if needed
# TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
from copy import deepcopy

import utils

ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf  # !!!!!


class SearchAlgos:
    def __init__(self, utility, succ, perform_move=None, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player, heuristic):
        pass


class MiniMax(SearchAlgos):
    def search(self, state, depth, maximizing_player, turn, end_time):
        """Start the MiniMax algorithm.
        :param turn: the current turn of the state
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if (end_time !=-1 and end_time <= time.time()):
            raise TimeOut

        if depth == 0  or self.goal(state,turn, maximizing_player)!=0 :
            if depth == 0:
                return self.utility(state, turn , maximizing_player) , state , False
            else:
                return  self.utility(state, turn , maximizing_player) , state , True

        children = self.succ(state[0], maximizing_player, turn)
        board_max = state
        end_game = False
        if maximizing_player:
            current_max = -np.inf
            for c in children:
                new_value , _ , is_endgame = self.search(c, depth - 1, not maximizing_player, turn + 1, end_time)
                if (current_max == -np.inf):
                    current_max = new_value
                    board_max = c
                    end_game = is_endgame
                elif current_max < new_value:
                    current_max = new_value
                    board_max = c
                    end_game = is_endgame
            return current_max , board_max , end_game

        else:
            current_min = np.inf
            for c in children:
                new_value, _  , is_endgame = self.search(c, depth - 1, not maximizing_player, turn + 1, end_time)
                if (current_min == np.inf):
                    current_min = new_value
                    board_max = c
                    end_game = is_endgame
                elif current_min > new_value:
                    current_min = new_value
                    board_max = c
                    end_game = is_endgame
            return current_min , board_max , end_game


class AlphaBeta(SearchAlgos):

    def search(self, state, depth, maximizing_player , turn , end_time, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT ):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if (end_time !=-1 and end_time <= time.time()):
            raise TimeOut
        if depth == 0  or self.goal(state,turn, maximizing_player)!=0 :
            if depth == 0:
                return self.utility(state, turn , maximizing_player) , state , False
            else:
                return  self.utility(state, turn , maximizing_player) , state , True

        children = self.succ(state[0], maximizing_player, turn)
        board_max = state
        end_game = False
        if maximizing_player:
            current_max = -np.inf
            for c in children:
                new_value , _  , is_endgame= self.search(c, depth - 1, not maximizing_player, turn + 1, end_time , alpha , beta)
                if (current_max == -np.inf):
                    current_max = new_value
                    board_max = c
                    end_game = is_endgame
                elif current_max < new_value:
                    current_max = new_value
                    board_max = c
                    end_game = is_endgame
                alpha = max(alpha, current_max)
                if(current_max >= beta):
                    return np.inf , c , is_endgame
            return current_max , board_max , end_game
        else:
            current_min = np.inf
            for c in children:
                new_value, _ , is_endgame = self.search(c, depth - 1, not maximizing_player, turn + 1, end_time)
                if (current_min == np.inf):
                    current_min = new_value
                    board_max = c
                    end_game = is_endgame
                elif current_min > new_value:
                    current_min = new_value
                    board_max = c
                    end_game = is_endgame
                beta = min(beta, current_min)
                if(current_min <= alpha):
                    return -np.inf , c , is_endgame
            return current_min , board_max , end_game



class TimeOut(Exception):
    pass
