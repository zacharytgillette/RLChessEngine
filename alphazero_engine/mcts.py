import torch
import math
import numpy as np
from state import *

class Node:
    def __init__(self, game, args, parent=None, action_taken=None, prior=0, state=None, visit_count=0):
        self.game = game
        self.args = args
        self.state = state # Not need until pass into model (post selection)
        self.parent = parent


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


    def initialize_node_state(self):

        parent = self.parent
        child_state = State(parent.state.T, parent.state)
        child_state = parent.game.get_next_state(child_state, self.action_taken)
        child_state = parent.game.change_perspective(child_state)

        self.state = child_state


    def expand_node(self, policy):
        for action, prob in enumerate(policy):

            if prob > 0:

                # child_state = State(self.state.T, self.state)
                # child_state = self.game.get_next_state(child_state, action)
                # child_state = self.game.change_perspective(child_state)
                child = Node(self.game, self.args, self, action, prob)
                self.children.append(child)

    def expand_root(self, policy):
        for action, prob in enumerate(policy):

            if prob > 0:

                child_state = State(self.state.T, self.state)
                child_state = self.game.get_next_state(child_state, action)
                child_state = self.game.change_perspective(child_state)
                child = Node(self.game, self.args, self, action, prob, state=child_state)
                self.children.append(child)

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1
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
        root = Node(self.game, self.args, state=state, visit_count=1)

        policy, _ = self.model(
            torch.tensor(self.game.get_encoded_state(state), device=self.model.device).unsqueeze(0)
        )
        policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()
        policy = (1 - self.args['dirichlet_epsilon']) * policy + self.args['dirichlet_epsilon'] \
                 * np.random.dirichlet([self.args['dirichlet_alpha']] * self.game.action_size)
        
        valid_moves = self.game.get_valid_moves(state)
      
        policy *= valid_moves
        policy /= np.sum(policy)

        root.expand_root(policy)

        count = 0

        for search in range(self.args['num_searches']):
            node = root

            count += 1

            while node.is_fully_expanded():
                node = node.select()

            # Copy state from parent, apply action, flip perspective, and add the state to the current node
            node.initialize_node_state()

            value, is_terminal = self.game.get_value_and_terminated(node.state, node.action_taken)
            value = self.game.get_opponent_value(value)

            if not is_terminal:
                policy, value = self.model(
                    torch.tensor(self.game.get_encoded_state(node.state), device=self.model.device).unsqueeze(0)
                )
                policy = torch.softmax(policy, axis=1).squeeze(0).cpu().numpy()

                valid_moves = self.game.get_valid_moves(node.state)

                policy *= valid_moves
                policy /= np.sum(policy)

                value = value.item()

                node.expand_node(policy)

            node.backpropagate(value)

        action_probs = np.zeros(self.game.action_size)
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        action_probs /= np.sum(action_probs)
        return action_probs
