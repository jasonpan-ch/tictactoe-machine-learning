import torch
from agent import Agent
from environment import TicTacToe

def print_board(board):
    symbols = {0: " ", 1: "O", 2: "X"}
    b = [symbols[cell] for cell in board]
    
    print(f"\n {b[0]} | {b[1]} | {b[2]} ")
    print("-----------")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("-----------")
    print(f" {b[6]} | {b[7]} | {b[8]} \n")

def main():
    env = TicTacToe()
    agent = Agent()
    
    try:
        agent.model.load_state_dict(torch.load("tic_tac_toe_model.pth")) # Loads the trained model
        agent.epsilon = 0  # no random moves
    except FileNotFoundError:
        print("Error: 'tic_tac_toe_model.pth' not found.")
        return

    state = env.reset()
    done = False
    print("Type a number 0-8")

    while not done:
        if env.current_player == 1:
            # --- AI'S TURN (Player 1) ---
            legal_moves = env.get_legal_moves()
            action = agent.select_action(state, legal_moves)
            state, reward, done = env.step(action)

            if done:
                if reward == 1:
                    print("AI won!")
                    print_board(state)
                else:
                    print("Draw!")
                    print_board(state)
                break
        else:
            # Player 2
            legal_moves = env.get_legal_moves()
            print(f"Legal moves left: {legal_moves}")
            print_board(state)
            
            move = -1
            while move not in legal_moves:
                try:
                    move = int(input("Enter your move (0-8): "))
                    if move not in legal_moves:
                        print("That spot is taken or invalid. Try again.")
                except ValueError:
                    print("Please enter a valid number between 0 and 8.")

            state, reward, done = env.step(move)
            
            if done:
                if reward == 1:
                    print("Congratulations! You won!")
                    print_board(state)
                else:
                    print("It's a draw!")
                    print_board(state)
                break

if __name__ == "__main__":
    main()