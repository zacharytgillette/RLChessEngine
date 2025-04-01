import torch
import math
import numpy as np

class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None, prior=0, visit_count=0):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent

        # TODO: Reflect action representation (post being decoded)
        self.action_taken = action_taken
        self.prior = prior

        self.children = []

        self.visit_count = visit_count
        self.value_sum = 0

    def is_fully_expanded(self):
        return len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        if child.visit_count == 0:
            q_value = 0
        else:
            q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * (math.sqrt(self.visit_count) / (child.visit_count + 1)) * child.prior

    def expand(self, policy):
        for action, prob in enumerate(policy):
            if prob > 0:
                child_state = self.state.copy()

                # Is the "get_next_state" called with player=1 bc it's representing the current player making the move? Like whoever is going to make the move, it's their turn, and we reflect that here as player 1 (regardless of whether player 1 or 2 are actually up).
                # We then switch perspective using player=-1 to show that we're changing the state because it will then be the next players turn, correct?

                # TODO: Repeats.
                child_state = self.game.get_next_state(child_state, action, 1)
                child_state = self.game.change_perspective(child_state, player=-1)

                child = Node(self.game, self.args, child_state, self, action, prob)
                self.children.append(child)

        return child

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        # Explain the switching of the value as we go up the tree in the context of switching perspective and the value and overall training the model on this switching player's turns as we build the tree (and go back up it here)
        # TODO: Repeat.
        value = self.game.get_opponent_value(value)
        if self.parent is not None:
            self.parent.backpropagate(value)


class MCTS:
    def __init__(self, game, args, model):
        self.game = game
        self.args = args
        self.model = model

    @torch.no_grad()
    def search(self, state):
        root = Node(self.game, self.args, state, visit_count=1)

        # Why don't we care about the value from the model here? We backpropagate the "value" up the tree in the search loop below. Why don't we care here?
        # Is it cause the value is used in the UCB scores and UCB isn't run on the root node, only the children and their children etc., and this whole search function is only meant to return the action_probs, not the value? I think so.
        policy, _ = self.model(
            torch.tensor(self.game.get_encoded_state(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.args['dirichlet_epsilon']) * policy + self.args['dirichlet_epsilon'] \
                 * np.random.dirichlet([self.args['dirichlet_alpha']] * self.game.action_size)

        # TODO: Get valid moves
        # Decoding model output and getting valid moves go hand in hand
        valid_moves = self.game.get_valid_moves(state)
        policy *= valid_moves
        policy /= np.sum(policy)

        root.expand(policy)

        for search in range(self.args['num_searches']):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            # I don't understand what "value" is here or why we "change the perspective" of the value (make it the opponents value). Why are we backpropagating a 1 or 0 that corresponds to the check win condition?
            # I see we use the "value" (poorly named as it causes confusion with this value) from the model below in the "if not is_terminal:" statement. Does that override this value? Is it just there so backpropogate function call doesn't error? So lost.

            # TODO: Whole consideration of changing the node structure to either not include action_taken or also include the player who made the move
            # Have to consider what we're going to represent the "action" as, either (1) the simple from, move, and piece type or (2) the fully decoded to and from bitboards (either 2 or 4 total)
            # In this conversation is also potentially making the slight alteration of including a "player" in the MCTS search

            # TODO: Repeat.
            value, is_terminal = self.game.get_value_and_terminated(node.state, node.action_taken)
            # TODO: Flipping the value (* -1)
            value = self.game.get_opponent_value(value)

            # If it is terminal, why don't we have a function that breaks from the "for search in range(self.args['num_searches']):" loop? does it not just run pointlessly then?
            # Is it cause we're just trying to build out a tree and not playing an actual game? And the "get_value" function call above is just meant to backpropogate a value of a win (1) if the action taken won? Why change perspective on the value (get_opponent_value) then?

            if not is_terminal:
                policy, value = self.model(
                    torch.tensor(self.game.get_encoded_state(node.state), device=self.model.device).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()

                # TODO: Repeat.
                valid_moves = self.game.get_valid_moves(node.state)
                policy *= valid_moves
                policy /= np.sum(policy)

                value = value.item()

                node.expand(policy)

            node.backpropagate(value)

        action_probs = np.zeros(self.game.action_size)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
