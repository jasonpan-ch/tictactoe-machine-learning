import torch

from agent import Agent
from environment import TicTacToe

env = TicTacToe()
agent = Agent()
episode = 20000

for e in range(episode):
    state = env.reset()
    done = False
    last_state = {1: None, 2: None}
    last_action = {1: None, 2: None}
    while not done:
        current_p = env.current_player
        legal_moves = env.get_legal_moves()
        action = agent.select_action(state, legal_moves)
        last_state[current_p] = state
        last_action[current_p] = action
        next_state, reward, done = env.step(action)
        
        if done:
            if reward == 1:
                agent.store_experience(last_state[current_p], last_action[current_p], 1, next_state, True)
                other_p = 3 - current_p
                if last_state[other_p] is not None:
                    agent.store_experience(last_state[other_p], last_action[other_p], -2, next_state, True)
            else:
                agent.store_experience(last_state[1], last_action[1], 0.5, next_state, True)
                agent.store_experience(last_state[2], last_action[2], 0.5, next_state, True)
        else:
            other_p = 3 - current_p
            if last_state[other_p] is not None:
                agent.store_experience(last_state[other_p], last_action[other_p], 0, next_state, False)
        agent.train()
        state = next_state
    if (e + 1) % 100 == 0: # Print progress every 100 episodes
        print(f"Episode {e+1}/{episode} | Epsilon: {agent.epsilon:.3f}")
torch.save(agent.model.state_dict(), "tic_tac_toe_model.pth") # Saves the trained model