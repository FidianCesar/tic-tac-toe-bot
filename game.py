import random
import numpy as np
import sys

class Game:
    def __init__(self):
        self.void_marker = 0
        self.player_1_marker = 1
        self.player_2_marker = 2
        self.reset_board()
        self.winning_positions = [[0, 1, 2],
                                  [3, 4, 5],
                                  [6, 7, 8],
                                  [0, 3, 6],
                                  [1, 4, 7],
                                  [2, 5, 8],
                                  [0, 4, 8],
                                  [2, 4, 6]]
        self.known_positions = {}
        self.turn_marker = random.choice([self.player_1_marker, self.player_2_marker])
        self.reward_max_marker = self.turn_marker
        

    def set_reward_max_marker(self, reward_max_marker):
        self.reward_max_marker = reward_max_marker # Which player should get the rewards for an ended game

    def reset_board(self):
        self.board = [self.void_marker] * 9

    def step(self, move, player_marker):
        self.turn_marker = 3 - self.turn_marker
        if self.board[move] != self.void_marker:
            if player_marker == self.reward_max_marker:
                return -10, True
            # if static bot, choose a random valid spot - otherwise no game can ever be finished as static bot never learns
            move = random.choice(self.get_possible_moves(self.board))
        self.board[move] = player_marker
        result = self.game_over(self.board, self.reward_max_marker)
        if result != None:
            return 9 * result * (1 + result) - 1, True
        return 0, False      

    def get_board_id(self, position):
        '''
        Gets the board id in ternary notation.
        '''
        board_id = 0
        exp = 0
        for marker in position:
            board_id += marker * 3 ** exp
            exp += 1
        return board_id

    def minimax(self, position, marker):
        board_id = self.get_board_id(position)
        if board_id in list(self.known_positions.keys()):
            return self.known_positions[board_id]
        result = self.game_over(position, marker)
        if result != None:
            self.known_positions[board_id] = result
            return result
        
        possible_moves = self.get_possible_moves(position)
        scores = []
        for move in possible_moves:
            new_position = position[::]
            new_position[move] = marker
            score = -self.minimax(new_position, 3 - marker)
            scores.append(score)
        result = max(scores)
        self.known_positions[board_id] = result
        return result

    def get_possible_moves(self, position):
        free_tiles = []
        for i in range(9):
            tile = position[i]
            if tile == self.void_marker:
                free_tiles.append(i)
        return free_tiles

    def play_good_move(self, marker):
        '''
        Plays the optimal move using minimax search at maximal depth. Does not take winning probabilities into account, only score:
        The choice between a move that leads to a single complicated winning line - everything else is a draw
        and a move that leads to a position, where there is a single complicated drawing line for the opponent - everything else is a win,
        will be made at random, as the outcomes are the same (the win can always be forced by this player, and the draw by the opponent).
        '''
        possible_moves = self.get_possible_moves(self.board)
        results = {}
        for move in possible_moves:
            new_position = self.board[::]
            new_position[move] = marker
            score = -self.minimax(new_position, 3 - marker)
            scores = list(results.keys())
            if score in scores: results[score].append(move)
            else: results[score] = [move]
        scores = list(results.keys())
        best_move = random.choice(results[max(scores)])
        self.board[best_move] = marker
        self.turn_marker = 3 - self.turn_marker

    def game_over(self, position, marker):
        if self.has_won(position, marker): return 1
        elif self.has_won(position, 3 - marker): return -1
        elif self.is_drawn(position): return 0

    def is_drawn(self, position):
        return self.void_marker not in position

    def has_won(self, proposed_position, player_marker):
        for position in self.winning_positions:
            if player_marker == proposed_position[position[0]] == proposed_position[position[1]] == proposed_position[position[2]]:
                return True
        return False

    def print_board(self, board):
        print('{}|{}|{}\n-----\n{}|{}|{}\n-----\n{}|{}|{}\n'.format(*board))


