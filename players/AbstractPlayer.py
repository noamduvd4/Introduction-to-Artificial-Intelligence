"""Abstract class of player. 
Your players classes must inherit from this.
"""
from copy import deepcopy

import utils
import numpy as np


class AbstractPlayer:
    """Your player must inherit from this class.
    Your player class name must be 'Player', as in the given examples (SimplePlayer, LivePlayer).
    Use like this:
    from players.AbstractPlayer import AbstractPlayer
    class Player(AbstractPlayer):
    """

    def __init__(self, game_time):
        """
        Player initialization.
        """
        self.game_time = game_time
        self.board = np.array(24)
        self.directions = utils.get_directions
        self.turn = None
        self.my_pos = None
        self.rival_pos = None

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array of the board.
        No output is expected.
        """
        self.board=board
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, (pos, soldier, dead_opponent_pos)
        """
        raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        raise NotImplementedError

    def is_player(self, player, pos1, pos2, board=None):
        """
        Function to check if 2 positions have the player on them
        :param player: 1/2
        :param pos1: position
        :param pos2: position
        :return: boolean value
        """
        if board is None:
            board = self.board
        if int(board[pos1]) == player and int(board[pos2]) == player:
            return True
        else:
            return False

    def check_next_mill(self, position, player, board=None):
        """
        Function to check if a player can make a mill in the next move.
        :param position: curren position
        :param board: np.array
        :param player: 1/2
        :return:
        """
        if board is None:
            board = self.board
        mill = [
            (self.is_player(player, 1, 2, board) or self.is_player(player, 3, 5, board)),
            (self.is_player(player, 0, 2, board) or self.is_player(player, 9, 17, board)),
            (self.is_player(player, 0, 1, board) or self.is_player(player, 4, 7, board)),
            (self.is_player(player, 0, 5, board) or self.is_player(player, 11, 19, board)),
            (self.is_player(player, 2, 7, board) or self.is_player(player, 12, 20, board)),
            (self.is_player(player, 0, 3, board) or self.is_player(player, 6, 7, board)),
            (self.is_player(player, 5, 7, board) or self.is_player(player, 14, 22, board)),
            (self.is_player(player, 2, 4, board) or self.is_player(player, 5, 6, board)),
            (self.is_player(player, 9, 10, board) or self.is_player(player, 11, 13, board)),
            (self.is_player(player, 8, 10, board) or self.is_player(player, 1, 17, board)),
            (self.is_player(player, 8, 9, board) or self.is_player(player, 12, 15, board)),
            (self.is_player(player, 3, 19, board) or self.is_player(player, 8, 13, board)),
            (self.is_player(player, 20, 4, board) or self.is_player(player, 10, 15, board)),
            (self.is_player(player, 8, 11, board) or self.is_player(player, 14, 15, board)),
            (self.is_player(player, 13, 15, board) or self.is_player(player, 6, 22, board)),
            (self.is_player(player, 13, 14, board) or self.is_player(player, 10, 12, board)),
            (self.is_player(player, 17, 18, board) or self.is_player(player, 19, 21, board)),
            (self.is_player(player, 1, 9, board) or self.is_player(player, 16, 18, board)),
            (self.is_player(player, 16, 17, board) or self.is_player(player, 20, 23, board)),
            (self.is_player(player, 16, 21, board) or self.is_player(player, 3, 11, board)),
            (self.is_player(player, 12, 4, board) or self.is_player(player, 18, 23, board)),
            (self.is_player(player, 16, 19, board) or self.is_player(player, 22, 23, board)),
            (self.is_player(player, 6, 14, board) or self.is_player(player, 21, 23, board)),
            (self.is_player(player, 18, 20, board) or self.is_player(player, 21, 22, board))
        ]

        return mill[position]

    def is_mill(self, position, board=None):
        if board is None:
            board = self.board
        """
        Return True if a player has a mill on the given position
        :param position: 0-23
        :return:
        """
        if position < 0 or position > 23:
            return False
        p = int(board[position])

        # The player on that position
        if p != 0:
            # If there is some player on that position
            return self.check_next_mill(position, p, board)
        else:
            return False

    def succ(self, board, maximizing_player, turn):
        player_number = 1
        rival_number = 2
        if not maximizing_player:
            player_number = 2
            rival_number = 1

        if turn >= 18:
            return self._succ_stage_2(board, player_number, rival_number)
        else:
            return self._succ_stage_1(board, player_number, rival_number)

    def _succ_stage_1(self, board, player_number, rival_number):
        board_list = []
        for pos in range(len(board)):
            if board[pos] != 0:
                continue
            board_dup = deepcopy(board)
            board_dup[pos] = player_number
            if self.is_mill(pos, board_dup):
                for rival_pos in range(len(board_dup)):
                    if int(board_dup[rival_pos]) == rival_number:
                        board_dup_dup = deepcopy(board_dup)
                        board_dup_dup[rival_pos] = 0
                        board_list.append([board_dup_dup, pos, rival_pos])
            else:
                board_dup[pos] = player_number
                board_list.append([board_dup, pos, -1])
        return board_list

    def _succ_stage_2(self, board, player_number, rival_number):
        board_list = []
        for old_pos in range(len(board)):
            if int(board[old_pos]) != player_number:
                continue
            directions = utils.get_directions(old_pos)
            for move_pos in directions:
                if board[move_pos] != 0:
                    continue
                board_dup = deepcopy(board)
                board_dup[move_pos] = player_number
                board_dup[old_pos] = 0
                if self.is_mill(move_pos, board_dup):
                    for rival_pos in range(len(board_dup)):
                        if int(board_dup[rival_pos]) == rival_number:
                            board_dup_dup = deepcopy(board_dup)
                            board_dup_dup[rival_pos] = 0
                            board_list.append([board_dup_dup, move_pos, rival_pos])
                else:
                    board_list.append([board_dup, move_pos, -1])
        return board_list

    def _get_positions(self, board, player_num):
        """
        Return an array in which player player_num`s pieces are
        """
        pos = [-1 for i in range(9)]
        index = 0
        for i in range(board.size):
            if int(board[i]) == player_num:
                pos[index] = i
                index += 1
        return pos

    def _get_my_pos(self, board):
        return self._get_positions(board, 1)

    def _get_rival_pos(self, board):
        return self._get_positions(board, 2)

    def _compere_move_to_board(self, state):
        """
        get state from the minmax algo and turn it to a valid move
        """
        new_board = state[0]
        new_pos = state[1]
        rival_cell = state[2]
        soldier_that_moved = 0
        if self.turn < 18:
            soldier_that_moved = int(np.where(self.my_pos == -1)[0][0])
            self.my_pos[soldier_that_moved] = new_pos
        else:
            for index in range(len(self.my_pos)):
                if int(self.my_pos[index]) >= 0 and int(new_board[self.my_pos[index]]) != 1:
                    self.board[self.my_pos[index]] = 0
                    self.my_pos[index] = new_pos
                    soldier_that_moved = index
                    break
        self.board[new_pos] = 1
        if int(rival_cell) != -1:
            rival_idx = np.where(self.rival_pos == int(rival_cell))[0][0]
            self.rival_pos[rival_idx] = -2
            self.board[rival_cell] = 0
        return new_pos, soldier_that_moved, rival_cell

    def _closed_mill(self, state) -> int:
        """
         Return 1 if the player last move created a mill
                -1 if the rival last move created a mill
                0 if the last move did not created a millß
         :param self , moved_cell
         """
        rival_eaten_locaton = state[2]
        last_move = state[1]
        board = state[0]
        if (int(rival_eaten_locaton) != -1 and int(board[last_move]) == 1):
            return 1
        elif (int(rival_eaten_locaton) != -1 and int(board[last_move]) == 2):
            return -1
        return 0

    def _number_of_player_pieces(self, player_number, state) -> int:
        """
         Return the number of the given player pieces left on the board
         :param self, player_number
         """
        board = state[0]
        counter = 0
        for pieces in board:
            if int(pieces) == player_number:
                counter += 1
        return counter

    def _number_of_player_pieces_hur(self, state) -> int:
        """
         Return the number of the agent pieces left - number of rival pieces left
         :param self, player_number
         """
        return self._number_of_player_pieces(1, state) - self._number_of_player_pieces(2, state)

    def _number_of_incomplete_mils_hur(self, state) -> int:
        """
         Return the number of the agent incomplete mills - number of rivel incomplete mills
         :param self
         """
        counter = 0
        board = state[0]
        for index in range(len(board)):
            if int(board[index]) == 0:
                if self.check_next_mill(index, 1 , board):
                    counter += 1
                elif self.check_next_mill(index, 2 , board):
                    counter -= 1
        return counter

    def _is_blocked(self, state, position) -> int:
        """
        Return True if the player that in position is blocked
        """
        board = state[0]
        directions = utils.get_directions(position)
        for cell in directions:
            if int(board[cell]) == 0:
                return False
        return True

    def _num_of_blocked_pieces(self, state, player_num) -> int:
        """
        Return the num of blocked pieces that player number player_num has
        """
        counter = 0
        if player_num == 1:
            positions = self._get_my_pos(state[0])
        else:  # player_num=2
            positions = self._get_rival_pos(state[0])
        for player in range(len(positions)):
            if int(positions[player]) != -1:
                if self._is_blocked(state, positions[player]):
                    counter += 1
        return counter

    def _diff_mine_and_opponent_blocked_pieces(self, state):
        """
        Return the diff between my blocked pieces to my opponent`s blocked pieces
        """
        return self._num_of_blocked_pieces(state, 2) - self._num_of_blocked_pieces(state, 1)

    def _number_of__player_mils(self,state,player):
        board = state[0]
        counter = 0
        for index in range(board.size):
            if (int(board[index]) == player and self.is_mill(index,board)):
                counter +=1
                direction = self.directions(index)
                is_double_mill = True
                for neb in direction:
                    if (int(board[neb])!= player or not self.is_mill(neb)):
                        is_double_mill = False
                        break
                if(is_double_mill):
                    counter += 1
        return  counter/3



    def _difftence_between_number_of_mills_hur(self,state):
        return self._number_of__player_mils(state,1) - self._number_of__player_mils(state,2)

    def goal(self, state ,turn, maximizing_player):
        """
        Return 1 if the state is a winning for the player, -1 if a winning for the rival, 0 otherwise
        """
        if turn < 18:
            return 0
        if self._num_of_blocked_pieces(state, 2) == self._number_of_player_pieces(2,state) and not maximizing_player:  # all the opponent`s pieces are blocked
            return 1
        elif self._num_of_blocked_pieces(state, 1) == self._number_of_player_pieces(1,state) and maximizing_player:  # all of my pieces are blocked
            return -1
        elif sum(pos != -1 for pos in self._get_rival_pos(state[0])) < 3:  # I won
            return 1
        elif sum(pos != -1 for pos in self._get_my_pos(state[0])) < 3:  # rival won
            return -1
        else:  # no winner
            return 0

    def _heuristic_stage_1(self, state ):
        return 18 * self._closed_mill(state) + 1 * self._diff_mine_and_opponent_blocked_pieces(state) + \
               9 * self._number_of_player_pieces_hur(state) + 10 * self._number_of_incomplete_mils_hur(state) + \
               26 * self._difftence_between_number_of_mills_hur(state)

    def _heuristic_stage_2(self, state , turn, maximizing_player):
        return 14 * self._closed_mill(state) + 10 * self._diff_mine_and_opponent_blocked_pieces(state) + \
               11 * self._number_of_player_pieces_hur(state) + 1086 * self.goal(state , turn, maximizing_player) + \
               46*self._difftence_between_number_of_mills_hur(state)

    def utility(self, state, turn , maximizing_player):
        if turn >= 18:
            return self._heuristic_stage_2(state ,turn, maximizing_player)
        else:
            return self._heuristic_stage_1(state)
