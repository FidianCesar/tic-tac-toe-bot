import numpy as np
import math
import matplotlib.pyplot as plt
import game
import sys

class Bot:
    def __init__(self):
        '''
        The dynamic bot will play against the static bot until it scores no loss against it. Then it will pass its Q-table to it and repeat.
        '''
        self.dynamic_bot_Q = np.zeros([3**9, 9])
        self.total_games = 0
        self.static_bot_Q = np.zeros([3**9, 9])

        self.learning_rate = 0.8
        self.discount_factor = 0.95
        
        for i in range(30000):
            if i % 3 == 0:
                print(i/300, '%')
            self.update_bots()

    def update_bots(self):
        self.train()
        self.static_bot_Q = np.copy(self.dynamic_bot_Q)
        
    def train(self, games=100):
        self.rew_list = []
        self.mean_list = []
        for i in range(games): self.train_a_game(1.0 / (1 + self.total_games))


    def train_a_game(self, exploration_parameter):
        new_game = game.Game()
        new_game.set_reward_max_marker(new_game.player_1_marker)
        done = False
        state = new_game.get_board_id(new_game.board)
        while not done:
            if new_game.turn_marker == new_game.player_1_marker: # Dynamic bot
                action = np.argmax(self.dynamic_bot_Q[state,:] + np.random.randn(1, 9) * exploration_parameter)
                reward, done = new_game.step(action, new_game.player_1_marker)
                state_1 = new_game.get_board_id(new_game.board)
                self.dynamic_bot_Q[state, action] = (1 - self.learning_rate) * self.dynamic_bot_Q[state, action]\
                                   + self.learning_rate * (reward + self.discount_factor * np.argmax(self.dynamic_bot_Q[state_1,:]))
                state = state_1
            else:
                action = np.argmax(self.static_bot_Q[state,:])
                reward, done = new_game.step(action, new_game.player_2_marker)
        self.total_games += 1
        self.rew_list.append(reward)
        self.mean_list.append(sum(self.rew_list)/len(self.rew_list))

if __name__ == '__main__':
    b = Bot()
    done = False
    new_game = game.Game()
    while not done: # Game not over
        print('Turn', new_game.turn_marker)
        if new_game.turn_marker == new_game.player_2_marker:
            action = np.argmax(b.dynamic_bot_Q[new_game.get_board_id(new_game.board),:])
            _, done = new_game.step(action, new_game.player_2_marker)
        else:
            new_game.print_board(new_game.board)
            player_move = int(input('Your move: '))
            if new_game.board[player_move] == new_game.void_marker:
                new_game.board[player_move] = new_game.player_1_marker
                new_game.turn_marker = 3 - new_game.turn_marker
            else:
                print('Illegal move, please retry!', file=sys.stderr)
                continue
        if None != new_game.game_over(new_game.board, new_game.player_1_marker):
            done = True
    print('End of game!')
    new_game.print_board(new_game.board)

