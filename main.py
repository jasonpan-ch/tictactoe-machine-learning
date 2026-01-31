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
    def step(self, action):
        