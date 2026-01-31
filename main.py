class TicTacToe:
    def __init__ (self):
        self.reset()
    def reset(self):
        self.board = [0 for _ in range(9)]
        self.current_player = 1
    def get_legal_moves(self):
        self.index = []
        for i in range(9):
            if self.board[i] == 0:
                self.index.append(i)
        return self.index
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
    def draw(self):
        if self.get_legal_moves() == [] and self.win() == 0:
            return True
        return False
    def step(self, action):
        if action not in self.get_legal_moves():
            raise ValueError("Invalid move")
        self.board[action] = self.current_player
        winner = self.win()
        is_draw = self.draw()
        self.current_player = 3 - self.current_player  # Switch player (1 -> 2, 2 -> 1)
        if winner != 0:
            self.reset()
            return winner
        elif is_draw == True:
            self.reset()
            return 3
        else:
            return 0