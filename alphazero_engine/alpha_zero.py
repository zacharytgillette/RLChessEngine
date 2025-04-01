from alphazero_engine.mcts import MCTS
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

        while True:
            # This is the start of me being confused about this whole changing perspective idea going on in building the tree and training the model. Why are we changing the perspective of the model here? It doesn't do anything on this first call though I guess since the player is 1.
            # Then it's purpose is to "orrient" the board for the current player (since they switch turns)

            # TODO: Flip bitboards betweeen players (W->B and B->W)
            neutral_state = self.game.change_perspective(state, player)

            # MCTS search returns the probabilities we should take a certain action (by selection a child node) by building the tree and then using the normalized visit counts of the root node's children.
            action_probs = self.mcts.search(neutral_state)

            memory.append((neutral_state, action_probs, player))

            temperature_action_probs = action_probs ** (1 / self.args['temperature'])
            # Does this sample based on probability distribution of the temperature_action_probs? or does it just take the highest one or something?
            action = np.random.choice(self.game.action_size, p=temperature_action_probs)

            # TODO: Decode action, decide representation of that action
            # Compare to 12 bitboards OR save 64 x 4 bits piece info

            # TODO: Make the action on the backend and return updated state
            state = self.game.get_next_state(state, action, player)

            # I understand the "value" here is used to save in the return memory as the value we're going to use MSE with the model's predicted value to improve the model, right?
            # I think part of my issue is the value idea is being used in different ways (though similar) in different places. Confusing.

            # TODO: Return if tie or win and if game ended
            value, is_terminal = self.game.get_value_and_terminated(state, action)

            if is_terminal:
                returnMemory = []
                for hist_neutral_state, hist_action_probs, hist_player in memory:
                    hist_outcome = value if hist_player == player else self.game.get_opponent_value(value)
                    returnMemory.append((
                        self.game.get_encoded_state(hist_neutral_state),
                        hist_action_probs,
                        hist_outcome
                    ))
                return returnMemory

            # TODO: Change player
            player = self.game.get_opponent(player)

    def train(self, memory):
        random.shuffle(memory)
        # We train on all contents of memory in the train function call correct?
        for batchIdx in range(0, len(memory), self.args['batch_size']):
            sample = memory[batchIdx:min(len(memory) - 1, batchIdx + self.args[
                'batch_size'])]  # Should I change this to memory[batchIdx:batchIdx+self.args['batch_size']] in case of an error?
            # The value_targets are just what i said from the return memory in the selfPlay class right? So for the state, if the player who's turn it was then, won, it is 1 and -1 if it the opponent won, given that there was a winner -- otherwise the value is 0 for a tie, correct?
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

            # What does "self.model.eval()" and "self.model.train()" do? Just change model settings?
            self.model.eval()
            for selfPlay_iteration in trange(self.args['num_selfPlay_iterations']):
                memory += self.selfPlay()

            self.model.train()
            # What are epochs, both in the traditional ML sense and here? I believe that the train function trains on all samples in memory; well then why train multiple times on the same data?
            for epoch in trange(self.args['num_epochs']):
                self.train(memory)

            # Can you give me a better idea of what the optimizer is? The model is just the weights correct? So then what's the optimizer?
            torch.save(self.model.state_dict(), f"model_{iteration}_{self.game}.pt")
            torch.save(self.optimizer.state_dict(), f"optimizer_{iteration}_{self.game}.pt")