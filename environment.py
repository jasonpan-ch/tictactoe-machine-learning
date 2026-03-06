import numpy as np

class TicTacToe:
    def __init__ (self):
        self.winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        self.reset()

    def reset(self):
        self.board = np.zeros(9, dtype=int)
        self.current_player = np.random.choice([1, 2])
        return self.board.copy()

    def get_legal_moves(self):
        return np.where(self.board == 0)[0].tolist()

    def win(self):
        for combo in self.winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != 0:
                return self.board[combo[0]]
        return 0
    
    def step(self, action):
        if self.board[action] != 0:
            return self.board.copy(), -1, True
        
        reward = 0

        self.board[action] = self.current_player
        done = False
        if self.win() != 0: # Rewards depending on who wins
            reward = 1
            done = True
        elif len(self.get_legal_moves()) == 0: # Checks for a draw
            done = True
        else:
            # Check if the move leaves the opponent with a winning move
            opponent = 3 - self.current_player
            for combo in self.winning_combinations:
                line = [self.board[i] for i in combo]
                if line.count(opponent) == 2 and line.count(0) == 1:
                    reward = -0.5
                    break
            self.current_player = 3 - self.current_player
        return self.board.copy(), reward, done