from alphazero_engine.game_functions import TicTacToe
from alphazero_engine.game_functions import ConnectFour
from alphazero_engine.alpha_zero import AlphaZero
from alphazero_engine.mcts import MCTS
from alphazero_engine.network import ResNet

import matplotlib.pyplot as plt
import torch
import numpy as np

class Test:
    def test_model(self):


        tictactoe = TicTacToe()

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        state = tictactoe.get_initial_state()
        state = tictactoe.get_next_state(state, 2, -1)
        state = tictactoe.get_next_state(state, 4, -1)
        state = tictactoe.get_next_state(state, 6, 1)
        state = tictactoe.get_next_state(state, 8, 1)

        encoded_state = tictactoe.get_encoded_state(state)

        tensor_state = torch.tensor(encoded_state, device=device).unsqueeze(0)

        model = ResNet(tictactoe, 4, 64, device=device)
        # model.load_state_dict(torch.load('model_2.pt', map_location=device))
        model.eval()

        policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()

        print(value)

        print(state)
        print(tensor_state)

        plt.bar(range(tictactoe.action_size), policy)
        plt.show()

    def test_selfplay(self):
        from alphazero_engine.game_functions import ConnectFour
        import torch

        game = ConnectFour()

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ResNet(game, 9, 128, device)

        optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

        args = {
            'C': 2,
            'num_searches': 600,
            'num_iterations': 8,
            'num_selfPlay_iterations': 500,
            'num_parallel_games': 100,
            'num_epochs': 4,
            'batch_size': 128,
            'temperature': 1.25,
            'dirichlet_epsilon': 0.25,
            'dirichlet_alpha': 0.3
        }

        alphaZero = AlphaZero(model, optimizer, game, args)
        alphaZero.learn()

    def test_play_model(self):
        game = ConnectFour()
        player = 1

        args = {
            'C': 2,
            'num_searches': 100,
            'dirichlet_epsilon': 0.,
            'dirichlet_alpha': 0.3
        }

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ResNet(game, 9, 128, device)
        # model.load_state_dict(torch.load("model_0_ConnectFour.pt", map_location=device))
        model.eval()

        mcts = MCTS(game, args, model)

        state = game.get_initial_state()

        while True:
            print(state)

            if player == 1:
                valid_moves = game.get_valid_moves(state)
                print("valid_moves", [i for i in range(game.action_size) if valid_moves[i] == 1])
                action = int(input(f"{player}:"))

                if valid_moves[action] == 0:
                    print("action not valid")
                    continue

            else:
                neutral_state = game.change_perspective(state, player)
                mcts_probs = mcts.search(neutral_state)
                action = np.argmax(mcts_probs)

            state = game.get_next_state(state, action, player)

            value, is_terminal = game.get_value_and_terminated(state, action)

            if is_terminal:
                print(state)
                if value == 1:
                    print(player, "won")
                else:
                    print("draw")
                break

            player = game.get_opponent(player)