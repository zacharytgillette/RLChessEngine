from game_functions import *
from alpha_zero import *
from network import *

import matplotlib.pyplot as plt
import torch
import numpy as np

class Test:
    def test_model(self):


        game = Chess(3)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        state = game.get_initial_state()
        state = game.get_next_state(state, 2)
        state = game.get_next_state(state, 4)
        state = game.get_next_state(state, 6)
        state = game.get_next_state(state, 8)

        encoded_state = game.get_encoded_state(state)

        tensor_state = torch.tensor(encoded_state, device=device).unsqueeze(0)

        model = ResNet(game, 4, 64, device=device)
        # model.load_state_dict(torch.load('model_2.pt', map_location=device))
        model.eval()

        policy, value = model(tensor_state)
        value = value.item()
        policy = torch.softmax(policy, axis=1).squeeze(0).detach().cpu().numpy()

        # print(value)

        # print(state)
        # print(tensor_state)

        plt.bar(range(game.action_size), policy)
        #plt.show()

    def test_selfplay(self):
        

        game = Chess(3)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ResNet(game, 20, 256, device)

        optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=0.0001)

        args = {
            'C': 2,
            'num_searches': 800,
            'num_iterations': 5,
            'num_selfPlay_iterations': 8,
            #'num_parallel_games': 100,
            'num_epochs': 5,
            'batch_size': 10,
            'temperature': 1.25,
            'dirichlet_epsilon': 0.25,
            'dirichlet_alpha': 0.3, 

        }

        alphaZero = AlphaZero(model, optimizer, game, args)
        alphaZero.learn()

    def test_play_model(self):
        game = Chess(3)
       
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

        initial_state = game.get_initial_state()
        state = game.get_initial_state()

        #for visualizer (purple squares, sounds)
        old_state = None
        capture = False
        castle = False


        while True:
            print(state)

            if player == 1:

                if initial_state.type_at_each_square == state.type_at_each_square:
                    print("TYPE AT EACH SQUARE THE SAME")
                    state.visualizer.visualize(state, -1, -1, make_move=True)
                else:
                    state = game.change_perspective(state)  

                    if castle and state.pieces[BLACK_KING].bitboard & 0x0200000000000000 > 0:
                        state.visualizer.visualize(state, 57, 58, make_move=True)
                    elif castle and state.pieces[BLACK_KING].bitboard & 0x2000000000000000 > 0:
                        state.visualizer.visualize(state, 60, 61, make_move=True)
                    else:
                        state.visualizer.visualize(state, diff[0], diff[1], make_move=True)

                    if capture:
                        state.visualizer.play_sound(1)
                    elif castle:
                        state.visualizer.play_sound(2)
                    else:
                        state.visualizer.play_sound(0)

                    
                    
                
                

                valid_moves = game.get_valid_moves(state)
                valid_indices = []
                for i in range(len(valid_moves)):
                    
                    if valid_moves[i] == 1:
                        valid_indices.append(i)



                print("valid_moves: from squares: ", [i%64 for i in range(game.action_size) if valid_moves[i] == 1])
                print("valid_moves: move type squares: ", [i//64 for i in range(game.action_size) if valid_moves[i] == 1])
                print("valid_moves: move type squares: ", [i for i in range(game.action_size) if valid_moves[i] == 1])

                #state.visualizer.visualize(state, 0, 0, make_move=True)

                action = state.visualizer.get_mouse_mouse(valid_indices, game.Left_Shift_to_Movement_type, state)


                #action = int(input(f"{player}:"))

                if valid_moves[action] == 0:
                    print("action not valid")
                    continue

            else:

                neutral_state = game.change_perspective(state)   

                #print("entering MCTS")
                mcts_probs = mcts.search(neutral_state)
                #print("exited MCTS")
                action = np.argmax(mcts_probs)

            #added for visualization
            old_state = State(state.T, state)
            num_empty_squares = old_state.type_at_each_square.count(-1)
        
            state = game.get_next_state(state, action)
            capture = num_empty_squares != state.type_at_each_square.count(-1)
            castle = 4 == state.count_differences(old_state)


            diff = [-1,-1]
            if old_state != None:
                diff = state.get_different_squares_between_states(old_state)

                if state.turn == BLACK:

                    #row_num = x // 8

                    diff[0] += (56 - ((diff[0] // 8)*16))
                    diff[1] += (56 - ((diff[1] // 8)*16))
                
            if state.turn == WHITE:

                if castle and state.pieces[WHITE_KING].bitboard & 0x0000000000000002 > 0:
                    state.visualizer.visualize(state, 1, 2, make_move=True)
                elif castle and state.pieces[WHITE_KING].bitboard & 0x0000000000000020 > 0:
                    state.visualizer.visualize(state, 4, 5, make_move=True)
                else:
                    state.visualizer.visualize(state, diff[0], diff[1], make_move=True)


                if capture:
                    state.visualizer.play_sound(1)
                elif castle:
                    state.visualizer.play_sound(2)
                else:
                    state.visualizer.play_sound(0)
            


            print("turn after GET NEXT STATE: ", state.turn)

            value, is_terminal = game.get_value_and_terminated(state, action)

            if is_terminal:
                print(state)
                if value == 1:
                    print(player, "won")
                    return 1
                else:
                    print("draw")
                    return 0
                # while True:
                #     state.visualizer.visualize(state, -1, -1, make_move=False, sound=False) 

            

            player = game.get_opponent(player)




    def test_play_model_mass_simulation(self):
        game = Chess(3)
       
        player = 1

        args = {
            'C': 2,
            'num_searches': 100,
            'dirichlet_epsilon': 0.25,
            'dirichlet_alpha': 0.3
        }

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model = ResNet(game, 20, 256, device)
        model.load_state_dict(torch.load("models/model_1_chess.pt", map_location=device))
        model.eval()

        mcts = MCTS(game, args, model)

        initial_state = game.get_initial_state()
        state = game.get_initial_state()

        #for visualizer (purple squares, sounds)
        old_state = None
        capture = False
        castle = False


        while True:
         

            neutral_state = state

            if player == 1:

                if initial_state.type_at_each_square == state.type_at_each_square:
                   
                    state.visualizer.visualize(state, -1, -1, make_move=True)
                else:

                    if castle and state.pieces[BLACK_KING].bitboard & 0x0200000000000000 > 0:
                        state.visualizer.visualize(state, 57, 58, make_move=True)
                    elif castle and state.pieces[BLACK_KING].bitboard & 0x2000000000000000 > 0:
                        state.visualizer.visualize(state, 60, 61, make_move=True)
                    else:
                        state.visualizer.visualize(state, diff[0], diff[1], make_move=True)

                    if capture:
                        state.visualizer.play_sound(1)
                    elif castle:
                        state.visualizer.play_sound(2)
                    else:
                        state.visualizer.play_sound(0)

                    
                    
                
                

                valid_moves = game.get_valid_moves(state)
                valid_indices = []
                for i in range(len(valid_moves)):
                    
                    if valid_moves[i] == 1:
                        valid_indices.append(i)


                mcts_probs = mcts.search(neutral_state)
             
                #TODO this is insanely bad
                action = np.random.choice(4672, p=mcts_probs)


            else:


                mcts_probs = mcts.search(neutral_state)
                #TODO this is insanely bad
                action = np.random.choice(4672, p=mcts_probs)

            #added for visualization
            old_state = State(state.T, state)
            num_empty_squares = old_state.type_at_each_square.count(-1)
        
            state = game.get_next_state(state, action)
            capture = num_empty_squares != state.type_at_each_square.count(-1)
            castle = 4 == state.count_differences(old_state)


            diff = [-1,-1]
            if old_state != None:
                diff = state.get_different_squares_between_states(old_state)

                if state.turn == BLACK:

                    #row_num = x // 8

                    if len(diff) < 2:
                        diff = [-1,-1]


                        print("WOAH WTF")
                        print("CURRENT STATE")
                        state.print_type_at_each_square()
                        counterrr = 0 
                        for item in state.queue:
                            print("history", counterrr)
                            counterrr += 1

                            State.print_pieces_from_bitboard(item[0])
                        state.print_type_at


                    else:
                        diff[0] += (56 - ((diff[0] // 8)*16))
                        diff[1] += (56 - ((diff[1] // 8)*16))
                
            if state.turn == WHITE:

                if castle and state.pieces[WHITE_KING].bitboard & 0x0000000000000002 > 0:
                    state.visualizer.visualize(state, 1, 2, make_move=True)
                elif castle and state.pieces[WHITE_KING].bitboard & 0x0000000000000020 > 0:
                    state.visualizer.visualize(state, 4, 5, make_move=True)
                else:
                    state.visualizer.visualize(state, diff[0], diff[1], make_move=True)


                if capture:
                    state.visualizer.play_sound(1)
                elif castle:
                    state.visualizer.play_sound(2)
                else:
                    state.visualizer.play_sound(0)
            


         

            value, is_terminal = game.get_value_and_terminated(state, action)

            if is_terminal:
           
                if value == 1:
                    print(player, "won")
                    return 1
                else:
                    print("draw")
                    return 0
                # while True:
                #     state.visualizer.visualize(state, -1, -1, make_move=False, sound=False) 

            

            player = game.get_opponent(player)
            state = game.change_perspective(state)  



            #state = game.change_perspective(state)




