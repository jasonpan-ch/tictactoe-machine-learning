import torch
import numpy as np

from agent import Agent
from environment import TicTacToe

def get_player_view(state, player):
    view = np.zeros_like(state)
    if player == 1:
        view[state == 1] = 1
        view[state == 2] = -1
    else:
        view[state == 2] = 1
        view[state == 1] = -1
    return view

env = TicTacToe()
agent = Agent()
episode = 20000

results = {"p1_wins": 0, "p2_wins": 0, "draws": 0}

for e in range(episode):
    state = env.reset()
    done = False
    last_state = {1: None, 2: None}
    last_action = {1: None, 2: None}
    last_reward = {1: 0, 2: 0}
    while not done:
        current_p = env.current_player
        legal_moves = env.get_legal_moves()
        
        # Get view for the agent (always sees 1 as self)
        current_view = get_player_view(state, current_p)
        action = agent.select_action(current_view, legal_moves)
        
        last_state[current_p] = state   
        last_action[current_p] = action
        next_state, reward, done = env.step(action)
        last_reward[current_p] = reward
        
        if done:
            if reward == 1:
                if current_p == 1: results["p1_wins"] += 1
                else: results["p2_wins"] += 1
            else:
                results["draws"] += 1
            # Store terminal experience for current player
            agent.store_experience(get_player_view(last_state[current_p], current_p), last_action[current_p], reward, get_player_view(next_state, current_p), True)
            
            # Store terminal experience for the other player (who lost or drew)
            other_p = 3 - current_p
            if last_state[other_p] is not None:
                # If current won (1), other lost (-1). If draw, other gets draw reward.
                other_reward = -1 if reward == 1 else 0.5
                agent.store_experience(get_player_view(last_state[other_p], other_p), last_action[other_p], other_reward, get_player_view(next_state, other_p), True)
        else:
            other_p = 3 - current_p
            if last_state[other_p] is not None:
                # Store experience for the previous player.
                agent.store_experience(get_player_view(last_state[other_p], other_p), last_action[other_p], last_reward[other_p], get_player_view(next_state, other_p), False)
        agent.train()
        state = next_state
    if (e + 1) % 100 == 0: # Print progress every 100 episodes
        message = f"""
              Episode {e+1}/{episode} | Epsilon: {agent.epsilon:.3f}
              P1: {results['p1_wins']} 
              P2: {results['p2_wins']} 
              Draws: {results['draws']} \n
"""
        print(message)
        results = {"p1_wins": 0, "p2_wins": 0, "draws": 0}

torch.save(agent.model.state_dict(), "tic_tac_toe_model.pth") # Saves the trained model