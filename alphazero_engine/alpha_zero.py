from mcts import *
import numpy as np
from tqdm import trange
import random
import torch
import torch.nn.functional as F


class AlphaZero:
    def __init__(self, model, optimizer, game, args):
        self.model = model
        self.optimizer = optimizer
        self.game = game
        self.args = args
        self.mcts = MCTS(game, args, model)

    def selfPlay(self):
        memory = []
        player = 1
        state = self.game.get_initial_state()

        count = 0

        while True:


            count += 1
            copy_state = State(state.T, state)

            # ----------------------------------------------------
            # TRY CATCH BLOCK HERE for mcts.search
            # We'll attempt up to 3 times to call self.mcts.search(...)
            # If all 3 fail, we re-raise the exception.
            # ----------------------------------------------------
            action_probs = None
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    action_probs = self.mcts.search(copy_state)
                    break  # Success: exit the retry loop
                except Exception as e:
                    print(f"[selfPlay] Error in mcts.search attempt {attempt+1}/{max_retries}: {e}")
                    if attempt == max_retries - 1:
                        # If it's still failing on the last attempt, re-raise
                        raise
                    # Otherwise, let it loop again to retry


            memory.append((copy_state, action_probs, player))


            temperature_action_probs = action_probs ** (1 / self.args['temperature'])
            temperature_action_probs /= np.sum(temperature_action_probs)
            action = np.random.choice(self.game.action_size, p=temperature_action_probs)

            state = self.game.get_next_state(state, action)
            value, is_terminal = self.game.get_value_and_terminated(state, action)
          

            if is_terminal:
                returnMemory = []
                for hist_copy_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    returnMemory.append((
                        self.game.get_encoded_state(hist_copy_state),
                        hist_action_probs,
                        hist_outcome
                    ))
                return returnMemory

     
            player = self.game.get_opponent(player)
            state = self.game.change_perspective(state)

    def train(self, memory):
        random.shuffle(memory)
        # We train on all contents of memory in the train function call correct?
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            # sample = memory[batchIdx:min(len(memory) - 1, batchIdx + self.args[
            #     'batch_size'])]  # Should I change this to memory[batchIdx:batchIdx+self.args['batch_size']] in case of an error?
            sample = memory[batchIdx : min(len(memory), batchIdx + self.args['batch_size'])]
            # # The value_targets are just what i said from the return memory in the selfPlay class right? So for the state, if the player who's turn it was then, won, it is 1 and -1 if it the opponent won, given that there was a winner -- otherwise the value is 0 for a tie, correct?
            state, policy_targets, value_targets = zip(*sample)

            state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(
                value_targets).reshape(-1, 1)

            state = torch.tensor(state, dtype=torch.float32, device=self.model.device)
            policy_targets = torch.tensor(policy_targets, dtype=torch.float32, device=self.model.device)
            value_targets = torch.tensor(value_targets, dtype=torch.float32, device=self.model.device)

            # This is part of the value question you'll see me asking throughout this codebase, but I want to make sure I fully understand what the out_value of the model is and what we're comparing (minimizing loss) it to
            out_policy, out_value = self.model(state)

            policy_loss = F.cross_entropy(out_policy, policy_targets)
            value_loss = F.mse_loss(out_value, value_targets)
            loss = policy_loss + value_loss
            # Could we benefit from ridge regularization here? Does the offical AlphaZero implementation have it?

            # Explain what the next three lines do? I get there're updating the model (and optimizer?) but what do they specifically do and also individually?
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    def learn(self):
        for iteration in range(self.args['num_iterations']):
            
            memory = []

            print("ITERATION", (iteration+1))
            
            

            # ----------------------------------------------------
            # TRY CATCH BLOCK HERE for selfPlay
            # We run selfPlay() multiple times; if an error occurs,
            # we'll log it and retry a few times so we don't skip an iteration.
            # ----------------------------------------------------
            self.model.eval()
            for selfPlay_iteration in trange(self.args['num_selfPlay_iterations']):
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        mem = self.selfPlay()
                        # If successful, add to memory and break retry loop
                        memory += mem
                        break
                    except Exception as e:
                        print(f"[learn] Error in selfPlay attempt {attempt+1}/{max_retries}: {e}")
                        if attempt == max_retries - 1:
                            # If it fails all attempts, re-raise or skip
                            raise
                        # else just loop again to retry
                

            self.model.train()
            print("training...")
            for epoch in trange(self.args['num_epochs']):
                print("epoch", (epoch+1))
                self.train(memory)
                

            torch.save(self.model.state_dict(), f"models/model_{iteration}_{self.game}.pt")
            torch.save(self.optimizer.state_dict(), f"models/optimizer_{iteration}_{self.game}.pt")