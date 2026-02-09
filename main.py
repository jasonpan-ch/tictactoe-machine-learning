import numpy as np

class TicTacToe:
    def __init__ (self):
        self.reset()

    def reset(self):
        self.board = np.zeros(9, dtype=int)
        self.current_player = 1
        return self.board.copy()

    def get_legal_moves(self):
        return np.where(self.board == 0)[0].tolist()

    def win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != 0:
                return self.board[combo[0]]
        return 0
    
    def step(self, action):
        if self.board[action] != 0:
            return self.board.copy(), -1, True
        self.board[action] = self.current_player
        winner = self.win()
        reward = 0
        done = False
        if winner != 0: # Rewards depending on who wins
            reward = 1
            done = True
        elif len(self.get_legal_moves()) == 0: # Checks for a draw
            reward = 0
            done = True
        else:
            self.current_player = 3 - self.current_player
        return self.board.copy(), reward, done