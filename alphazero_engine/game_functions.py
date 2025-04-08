# from game import Game  # Import backend Game class
import numpy as np
from state import *

'''
MADE A COPY OF THE TICTACTOE CLASS WITH TO-DO COMMENTS
'''
class Chess:
    def __init__(self, T):
        self.row_count = 8 
        self.column_count = 8 
        self.action_size = self.row_count * self.column_count * 73
        self.T = T

        self.Left_Shift_to_Movement_type = {

            8: 0,
            16: 1,
            24: 2,
            32: 3,
            40: 4, 
            48: 5,
            56: 6,

            7: 7, #up right
            14: 8,
            21: 9,
            28: 10,
            35: 11,
            42: 12,
            49: 13,

            -1: 14,
            -2: 15,
            -3: 16,
            -4: 17,
            -5: 18,
            -6: 19,
            -7: 20,

            -9: 21,
            -18: 22,
            -27: 23,
            -36: 24,
            -45: 25,
            -54: 26,
            -63: 27,

            -8: 28,
            -16: 29,
            -24: 30,
            -32: 31,
            -40: 32,
            -48: 33,
            -56: 34,

            -7: 35, 
            -14: 36, 
            -21: 37, 
            -28: 38, 
            -35: 39, 
            -42: 40, 
            -49: 41,

            1: 42,
            2: 43,
            3: 44,
            4: 45,
            5: 46,
            6: 47,
            7: 48, #left shift 6

            9: 49,
            18: 50,
            27: 51,
            36: 52,
            45: 53,
            54: 54,
            63: 55,

            # knight 
            15: 56,
            6: 57,
            -10: 58,
            -17: 59,
            -15: 60,
            -6: 61,
            10: 62,
            17: 63



        }


        self.Index_to_Movement_type = {

            #0-55: queen moves
            #up
            0: lambda x: x << 8,
            1: lambda x: x << 16,
            2: lambda x: x << 24,
            3: lambda x: x << 32,
            4: lambda x: x << 40,
            5: lambda x: x << 48,
            6: lambda x: x << 56,

            #up-right
            7: lambda x: x << 7,
            8: lambda x: x << 14,
            9: lambda x: x << 21,
            10: lambda x: x << 28,
            11: lambda x: x << 35,
            12: lambda x: x << 42,
            13: lambda x: x << 49,

            #right
            14: lambda x: x >> 1,
            15: lambda x: x >> 2,
            16: lambda x: x >> 3,
            17: lambda x: x >> 4,
            18: lambda x: x >> 5,
            19: lambda x: x >> 6,
            20: lambda x: x >> 7,

            #down-right
            21: lambda x: x >> 9,
            22: lambda x: x >> 18,
            23: lambda x: x >> 27,
            24: lambda x: x >> 36,
            25: lambda x: x >> 45,
            26: lambda x: x >> 54,
            27: lambda x: x >> 63,

            #down
            28: lambda x: x >> 8,
            29: lambda x: x >> 16,
            30: lambda x: x >> 24,
            31: lambda x: x >> 32,
            32: lambda x: x >> 40,
            33: lambda x: x >> 48,
            34: lambda x: x >> 56,

            #down-left
            35: lambda x: x >> 7,
            36: lambda x: x >> 14,
            37: lambda x: x >> 21,
            38: lambda x: x >> 28,
            39: lambda x: x >> 35,
            40: lambda x: x >> 42,
            41: lambda x: x >> 49,
            
            #left
            42: lambda x: x << 1,
            43: lambda x: x << 2,
            44: lambda x: x << 3,
            45: lambda x: x << 4,
            46: lambda x: x << 5,
            47: lambda x: x << 6,
            48: lambda x: x << 7,

            #top left
            49: lambda x: x << 9,
            50: lambda x: x << 18,
            51: lambda x: x << 27,
            52: lambda x: x << 36,
            53: lambda x: x << 45,
            54: lambda x: x << 54,
            55: lambda x: x << 63,



            #56-63: knight moves
            56: lambda x: x << 15,
            57: lambda x: x << 6,
            58: lambda x: x >> 10,
            59: lambda x: x >> 17,
            60: lambda x: x >> 15,
            61: lambda x: x >> 6,
            62: lambda x: x << 10,
            63: lambda x: x << 17,



            #64-72: underpromotions
            64: lambda x: x << 9,
            65: lambda x: x << 8,
            66: lambda x: x << 7,
            67: lambda x: x << 9,
            68: lambda x: x << 8,
            69: lambda x: x << 7,
            70: lambda x: x << 9,
            71: lambda x: x << 8,
            72: lambda x: x << 7

        }

    def __repr__(self):
        return "chess"

    # Backend, we have a state class and node's are objects of that class
    def get_initial_state(self):
        return State(self.T)

    def get_next_state(self, state, action):


        # Cast action to an int incase it is a numpy.int64 instead
        action = int(action)

        # Assuming "action" is a NUMBER from the mcts output
        from_square = action % 64
        movement_type = action // 64

        #translates the movement type into a bitshifting function
        # (which we call below on the piece to move it to its next spot)
        movement_function = self.Index_to_Movement_type[movement_type]

        #bitboard of FROM square
        from_bitboard = 0b1 << (from_square)
        #bitboard of TO square (apply the movement function)
        to_bitboard = movement_function(from_bitboard)

        #determine piece type
        from_piece_type = state.type_at_each_square[from_square]


        #Bitboard.print(state.pieces[from_piece_type].bitboard, "BEFORE")


        #DEBUGGING
        if from_piece_type not in state.pieces:
            Bitboard.print(from_bitboard, "FROM BITBOARD")
            Bitboard.print(to_bitboard, "TO BITBOARD")
            state.print_type_at_each_square()
            print("FROM PIECE TYPE", from_piece_type)


            counterrr = 0 
            print("CURRENT STATE")
            state.print_type_at_each_square()
            for item in state.queue:
                print("history", counterrr)
                counterrr += 1

                State.print_pieces_from_bitboard(item[0])



            while True:
                 state.visualizer.visualize(state, -1, -1, make_move=False, sound=False) 

        '''
        UPDATING STATE BITBOARDS
        '''

        #update state by...
        #... 1: masking out piece's "old" position (the from_bitboard)
        state.pieces[from_piece_type].bitboard &= Bitboard.complement(from_bitboard)
        #... 2: mask IN the piece's "new" position (the to_bitboard)
        state.pieces[from_piece_type].bitboard |= to_bitboard

        #edge case 1: CASTLING
        #if two-square move occured AND it was a king, then it was a castle
        #white, king-side (short) castle
        if from_piece_type == WHITE_KING and movement_type == 15:
            #update rook
            state.pieces[WHITE_ROOK].bitboard &= 0xfffffffffffffffe #remove rook in corner
            state.pieces[WHITE_ROOK].bitboard |= 0x0000000000000004 #add to new position

        #white, queen-side (long) castle
        elif from_piece_type == WHITE_KING and movement_type == 43:
            #update rook
            state.pieces[WHITE_ROOK].bitboard &= 0xffffffffffffff7f #remove rook in corner
            state.pieces[WHITE_ROOK].bitboard |= 0x0000000000000010 #add to new position

        #edge case 2: CAPTURING
        #determine if capture has occured by...
        capture_flag = False
        #... 1: determine the index of the piece in its "new" position
        to_square = to_bitboard.bit_length() -1
        #... 2: checking that index to see if an opponent piece is there
        to_piece_type = state.type_at_each_square[to_square]
        if to_piece_type != -1:

            #capture occured
            capture_flag = True
            #update state: mask out captured piece from its bitboard
            state.pieces[to_piece_type].bitboard &= Bitboard.complement(to_bitboard)

        #edge case 3: EN PASSANT
        en_passant_flag = False
        if state.en_passant_flags > 0 and from_piece_type == WHITE_PAWN and not capture_flag:
            
            en_passant_bitboard = state.en_passant_flags << 40
            if (en_passant_bitboard & to_bitboard) > 0:
                state.pieces[BLACK_PAWN].bitboard &= Bitboard.complement(en_passant_bitboard >> 8)
                en_passant_flag = True


        #edge case 4: PROMOTIONS
        promotion_flag = None
        if movement_type in [64, 65, 66]: 
            #add knight
            state.pieces[WHITE_KNIGHT].bitboard |= to_bitboard
            #remove pawn
            state.pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_KNIGHT
        elif movement_type in [67, 67, 69]: 
            #add bishop
            state.pieces[WHITE_BISHOP].bitboard |= to_bitboard
            #remove pawn
            state.pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_BISHOP
        elif movement_type in [70, 71, 72]: 
            #add rook
            state.pieces[WHITE_ROOK].bitboard |= to_bitboard
            #remove pawn
            state.pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_ROOK
        elif from_piece_type == WHITE_PAWN and movement_type in [0, 7, 49] and (to_bitboard & 0xff00000000000000 > 0):
            #add queen (THIS IS BASICALLY HARD-CODED FOR USER'S SIDE)
            state.pieces[WHITE_QUEEN].bitboard |= to_bitboard
            #remove pawn
            state.pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_QUEEN

        '''
        UPDATING STATE 'type_at_each_square'
        '''

        #remove piece from where it was...
        state.type_at_each_square[from_square] = -1
        #... and add the piece where it ends up
        state.type_at_each_square[to_square] = from_piece_type #handles edge case 2: CAPTURES

        #edge case 1: CASTLE
        if from_piece_type == WHITE_KING and movement_type == 15:
            #remove rook king-side
            state.type_at_each_square[0] = -1
            #place rook at new spot
            state.type_at_each_square[2] = WHITE_ROOK
        elif from_piece_type == WHITE_KING and movement_type == 43:
            #remove rook queen-side
            state.type_at_each_square[7] = -1
            #place rook at new spot
            state.type_at_each_square[4] = WHITE_ROOK

        #edge case 3: EN PASSANT
        if en_passant_flag:
            state.type_at_each_square[to_square - 8] = -1

        #edge case 4: PROMOTIONS
        if promotion_flag != None:
            state.type_at_each_square[to_square] = promotion_flag

        
        '''
        UPDATING STATE FLAGS
        '''

        # Preprocessing repeated moves
        if capture_flag or from_piece_type == WHITE_PAWN:
            state.repeated_moves = {}
        #first, concat. bitboards...
        concat_bitboards = ""
        for piece_type in state.pieces:
            concat_bitboards += Bitboard.to_string(state.pieces[piece_type].bitboard) + '$'
        #then, add to hash
        if concat_bitboards in state.repeated_moves:
            state.repeated_moves[concat_bitboards] += 1
        else:
            state.repeated_moves[concat_bitboards] = 1


        # Update flags

        #repeated moves
        if state.repeated_moves[concat_bitboards] == 2:
            state.repeated_moves_flags = 0b01
        elif state.repeated_moves[concat_bitboards] == 3:
            state.repeated_moves_flags = 0b10

        #en passant: might it be possible for next player, since current one did a double pawn move
        if from_piece_type == WHITE_PAWN and movement_type == 1: #if double move was made by pawn
            state.en_passant_flags = to_bitboard >> 24
        else:
            state.en_passant_flags = 0b0
  
        #castle flags
        if state.castle_flags > 0:
            if from_piece_type == WHITE_KING and state.turn == WHITE:
                #WHITE king moved, can't castle anymore
                state.castle_flags &= 0b1100
            elif from_piece_type == WHITE_KING and state.turn == BLACK:
                #BLACK king moved, can't castle anymore
                state.castle_flags &= 0b0011
            elif from_piece_type == WHITE_ROOK and from_bitboard & 0x0000000000000001 > 0 and state.turn == WHITE:
                #king-side WHITE rook moved, can't castle that side anymore
                state.castle_flags &= 0b1101
            elif from_piece_type == WHITE_ROOK and from_bitboard & 0x0000000000000080 > 0 and state.turn == WHITE:
                #queen-side WHITE rook moved, can't castle that side anymore
                state.castle_flags &= 0b1110
            elif from_piece_type == WHITE_ROOK and from_bitboard & 0x0000000000000001 > 0 and state.turn == BLACK:
                #king-side BLACK rook moved, can't castle that side anymore
                state.castle_flags &= 0b0111
            elif from_piece_type == WHITE_ROOK and from_bitboard & 0x0000000000000080 > 0 and state.turn == BLACK:
                #queen-side BLACK rook moved, can't castle that side anymore
                state.castle_flags &= 0b1011

        #total move count (after black moves, full turn has completed)
        if state.turn == BLACK:
            state.total_move_flags += 1

        #no progress count
        if from_piece_type == WHITE_PAWN or from_piece_type == BLACK_PAWN or capture_flag:
            if state.turn == WHITE:
                state.no_progress_color_flags = 1
            else:
                state.no_progress_color_flags = -1
            state.no_progress_flags = 0
        elif state.turn == state.no_progress_color_flags:
            state.no_progress_flags += 1

        '''
        SAVE HISTORY
        '''

        state.queue.popleft()
        state.queue.append([State.pieces_deep_copy_other(state.pieces), state.repeated_moves_flags])
       

        return state
        

    def temp_apply_action_to_bitboard(self, state_pieces, state, action):

        # Cast action to an int incase it is a numpy.int64 instead
        action = int(action)

        # Assuming "action" is a NUMBER from the mcts output
        from_square = action % 64
        movement_type = action // 64

        #translates the movement type into a bitshifting function
        # (which we call below on the piece to move it to its next spot)
        movement_function = self.Index_to_Movement_type[movement_type]

        #bitboard of FROM square
        from_bitboard = 0b1 << (from_square)
        #bitboard of TO square (apply the movement function)
        to_bitboard = movement_function(from_bitboard)

        #determine piece type
        from_piece_type = state.type_at_each_square[from_square]



        '''
        UPDATING STATE BITBOARDS
        '''

        #update state by...
        #... 1: masking out piece's "old" position (the from_bitboard)
        state_pieces[from_piece_type].bitboard &= Bitboard.complement(from_bitboard)
        #... 2: mask IN the piece's "new" position (the to_bitboard)
        state_pieces[from_piece_type].bitboard |= to_bitboard

        #edge case 1: CASTLING
        #if two-square move occured AND it was a king, then it was a castle
        #white, king-side (short) castle
        if from_piece_type == WHITE_KING and movement_type == 15:
            #update rook
            state_pieces[WHITE_ROOK].bitboard &= 0xfffffffffffffffe #remove rook in corner
            state_pieces[WHITE_ROOK].bitboard |= 0x0000000000000004 #add to new position

        #white, queen-side (long) castle
        elif from_piece_type == WHITE_KING and movement_type == 43:
            #update rook
            state_pieces[WHITE_ROOK].bitboard &= 0xffffffffffffff7f #remove rook in corner
            state_pieces[WHITE_ROOK].bitboard |= 0x0000000000000010 #add to new position

        #edge case 2: CAPTURING
        #determine if capture has occured by...
        capture_flag = False
        #... 1: determine the index of the piece in its "new" position
        to_square = to_bitboard.bit_length() -1
        #... 2: checking that index to see if an opponent piece is there
        to_piece_type = state.type_at_each_square[to_square]
        if to_piece_type != -1:

            #capture occured
            capture_flag = True
            #update state: mask out captured piece from its bitboard
            state_pieces[to_piece_type].bitboard &= Bitboard.complement(to_bitboard)

        #edge case 3: EN PASSANT
        en_passant_flag = False
        if state.en_passant_flags > 0 and from_piece_type == WHITE_PAWN and not capture_flag:
            
            en_passant_bitboard = state.en_passant_flags << 40
            if (en_passant_bitboard & to_bitboard) > 0:
                state_pieces[BLACK_PAWN].bitboard &= Bitboard.complement(en_passant_bitboard >> 8)
                en_passant_flag = True


        #edge case 4: PROMOTIONS
        promotion_flag = None
        if movement_type in [64, 65, 66]: 
            #add knight
            state_pieces[WHITE_KNIGHT].bitboard |= to_bitboard
            #remove pawn
            state_pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_KNIGHT
        elif movement_type in [67, 67, 69]: 
            #add bishop
            state_pieces[WHITE_BISHOP].bitboard |= to_bitboard
            #remove pawn
            state_pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_BISHOP
        elif movement_type in [70, 71, 72]: 
            #add rook
            state_pieces[WHITE_ROOK].bitboard |= to_bitboard
            #remove pawn
            state_pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_ROOK
        elif from_piece_type == WHITE_PAWN and movement_type in [0, 7, 49] and (to_bitboard & 0xff00000000000000 > 0):
            #add queen (THIS IS BASICALLY HARD-CODED FOR USER'S SIDE)
            state_pieces[WHITE_QUEEN].bitboard |= to_bitboard
            #remove pawn
            state_pieces[WHITE_PAWN].bitboard &= Bitboard.complement(to_bitboard)
            #update promotion flag
            promotion_flag = WHITE_QUEEN

        return state_pieces



    # TODO: Major discussion point
    def get_valid_moves(self, state):
        valid_indices = []

        #find all valid indices HERE
        white_pieces = [WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING]
        for piece_type in white_pieces:

            piece_obj = state.pieces[piece_type]
            important_moves = self.get_important_squares(state.pieces, BLACK)
            piece_moves = piece_obj.all_moves(important_moves[0], important_moves[1]) #list of bitboards of all post-moves


            #if piece is a king, then check castle
            local_castle_flag = state.castle_flags
            if state.turn == BLACK:
                local_castle_flag = local_castle_flag >> 2

            if piece_type == WHITE_KING and 0b0011 & local_castle_flag > 0:

                #logic for queen-side castle
                if 0b0001 & local_castle_flag > 0:


                    #TODO: for now, assume checking is not issue (fix this later)
                    if state.type_at_each_square[4] == -1 and state.type_at_each_square[5] == -1 and state.type_at_each_square[6] == -1:

                        #first, check if in check NOW
                        currently_in_check_flag = self.is_in_check(state.pieces, WHITE)
                        
                        #then, check if in check after FIRST step
                        state.pieces[WHITE_KING].bitboard = state.pieces[WHITE_KING].bitboard << 1
                        then_in_check_flag = self.is_in_check(state.pieces, WHITE)
                        state.pieces[WHITE_KING].bitboard = state.pieces[WHITE_KING].bitboard >> 1

                        if not (currently_in_check_flag or then_in_check_flag):

                            piece_moves += [0x0000000000000020]

                #logic for king-side castle
                if 0b0010 & local_castle_flag > 0:

                    #TODO: for now, assume checking is not issue (fix this later)
                    if state.type_at_each_square[1] == -1 and state.type_at_each_square[2] == -1:

                        #first, check if in check NOW
                        currently_in_check_flag = self.is_in_check(state.pieces, WHITE)
                        
                        #then, check if in check after FIRST step
                        state.pieces[WHITE_KING].bitboard = state.pieces[WHITE_KING].bitboard >> 1
                        then_in_check_flag = self.is_in_check(state.pieces, WHITE)
                        state.pieces[WHITE_KING].bitboard = state.pieces[WHITE_KING].bitboard << 1

                        if not (currently_in_check_flag or then_in_check_flag):


                            piece_moves += [0x0000000000000002]




            #if piece is a pawn, then check en passant
            if piece_type == WHITE_PAWN and state.en_passant_flags > 0:

           

                en_passant_bitboard = state.en_passant_flags << 32

                left_en_passant_bitboard = (en_passant_bitboard << 1) & 0xfefefefefefefefe
                right_en_passant_bitboard = (en_passant_bitboard >> 1) & 0x7f7f7f7f7f7f7f7f

                possible_left_pawn = state.pieces[WHITE_PAWN].bitboard & left_en_passant_bitboard
                possible_right_pawn = state.pieces[WHITE_PAWN].bitboard & right_en_passant_bitboard

                if possible_left_pawn > 0:
                    new_move = (state.pieces[WHITE_PAWN].bitboard & Bitboard.complement(possible_left_pawn)) | (en_passant_bitboard << 8)
                    piece_moves += [new_move]
              

                if possible_right_pawn > 0:
                    new_move = (state.pieces[WHITE_PAWN].bitboard & Bitboard.complement(possible_right_pawn)) | (en_passant_bitboard << 8)
                    piece_moves += [new_move]
                



            for current_bitboard in piece_moves:


                #START DECODING PIECE MOVES

                previous_bitboard = state.pieces[piece_type].bitboard
                
                from_bitboard = (previous_bitboard ^ current_bitboard) & previous_bitboard
                to_bitboard = (previous_bitboard ^ current_bitboard) & current_bitboard   # = 0 in bug

                #either both all 0s or identical


                left_shift_amount = to_bitboard.bit_length() - from_bitboard.bit_length()


                #DEBUGGING
                if left_shift_amount not in self.Left_Shift_to_Movement_type:

                    print("left shift amount (not in map)")

                    print("left shift amount", left_shift_amount)

                    print("piece type: ", piece_obj.print_piece_type(piece_type))

                    Bitboard.print(from_bitboard, "FROM BITBOARD")
                    Bitboard.print(to_bitboard, "TO BITBOARD")


                #for duplicates, determine which is the legal move
                #6s



                #7s
                if left_shift_amount == 7:

                    if from_bitboard & 0x0101010101010101 > 0:
                        move_type = 48
                    else:
                        move_type = 7

                elif left_shift_amount == -7:

                    if from_bitboard & 0x8080808080808080 > 0:
                        move_type = 20
                    else:
                        move_type = 35

                elif left_shift_amount == 6:

                    if from_bitboard & 0x0303030303030303 and piece_type != WHITE_KNIGHT:
                        move_type = 47
                    else:
                        move_type = 57
                
                elif left_shift_amount == -6 and piece_type != WHITE_KNIGHT:

                    if from_bitboard & 0xc0c0c0c0c0c0c0c0:
                        move_type = 19
                    else:
                        move_type = 61

                else:
                    #TODO: find better fix for strange rook/queen bug, also king one
                    #RANDOM PHYSICAL MOVE GENERATION ERROR; QUICK PATCH
                    if piece_type in [WHITE_ROOK, WHITE_QUEEN] and abs(left_shift_amount) > 7 and abs(left_shift_amount) % 8 == 7:
                        move_type = -666

                    elif left_shift_amount == 0:
                        move_type = -666

                    else:
                        move_type = self.Left_Shift_to_Movement_type[left_shift_amount]

                if move_type == -666:
                    continue

                from_square = from_bitboard.bit_length() - 1

                action = (move_type * 64) + from_square

                #CHECK if move puts us into check

                

                pieces_copy = State.pieces_deep_copy_other(state.pieces)
                pieces_copy = self.temp_apply_action_to_bitboard(pieces_copy, state, action) 

                if self.is_in_check(pieces_copy, WHITE):
                    continue

                # Move is good so add
                valid_indices.append(action)

                #additional promotion actions
                if piece_type == WHITE_PAWN and to_bitboard & 0xff00000000000000 > 0:
                    if left_shift_amount == 9:
                        action = (64 * 64) + from_square
                        valid_indices += [action]
                        action = (67 * 64) + from_square
                        valid_indices += [action]
                        action = (70 * 64) + from_square
                        valid_indices += [action]
                    elif left_shift_amount == 8:
                        action = (65 * 64) + from_square
                        valid_indices += [action]
                        action = (68 * 64) + from_square
                        valid_indices += [action]
                        action = (71 * 64) + from_square
                        valid_indices += [action]
                    elif left_shift_amount == 7:
                        action = (66 * 64) + from_square
                        valid_indices += [action]
                        action = (69 * 64) + from_square
                        valid_indices += [action]
                        action = (72 * 64) + from_square
                        valid_indices += [action]


        #from_square = action % 64
        #movement_type = action // 64
        
        #return in correct format
        mask = np.zeros(self.action_size, dtype=np.uint8)
        mask[valid_indices] = 1
        return mask

        # return (state.reshape(-1) == 0).astype(np.uint8)



    def get_important_squares(self, state_pieces, color):

        attacking_color = color * -1

        attacking_pieces = [WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN]
        defending_pieces = [BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING]
        if attacking_color == BLACK:
            attacking_pieces = [BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN]
            defending_pieces = [WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING]

        
        empty_squares = 0x0
        enemy_pieces = 0x0

        for piece_type in state_pieces:

            empty_squares |= state_pieces[piece_type].bitboard
            
            #only add defending (enemy) pieces to enemy_pieces bitboard
            if piece_type in defending_pieces:
                enemy_pieces |= state_pieces[piece_type].bitboard


        empty_squares = Bitboard.complement(empty_squares)



        return [empty_squares, enemy_pieces]





                        #color of king to see if he is in check
    def is_in_check(self, state_pieces, color):

        attacking_color = color * -1

        color_king = BLACK_KING

        attacking_pieces = [WHITE_PAWN, WHITE_KNIGHT, WHITE_BISHOP, WHITE_ROOK, WHITE_QUEEN, WHITE_KING]
        if attacking_color == BLACK:
            color_king = WHITE_KING
            attacking_pieces = [BLACK_PAWN, BLACK_KNIGHT, BLACK_BISHOP, BLACK_ROOK, BLACK_QUEEN, BLACK_KING]
        
        
        #check if these piece's next-move's bitboards overlap with king
        #NEW: if mate=True, then ALL moves must leave king in check, not just one
        for piece_type in attacking_pieces:

            piece_obj = state_pieces[piece_type]

            important_squares = self.get_important_squares(state_pieces, color)

            all_moves = piece_obj.all_moves(important_squares[0], important_squares[1])

            for move in all_moves:

                if move & state_pieces[color_king].bitboard > 0:

                    return True
                
        return False








    # TODO: Leddon will handle this once Zach has work done, will have to pass in another parameter of the player
    # Description: Did the player who made the last move win?
    def check_win(self, state, action):
        # TODO: What would this look like if bitboards are used?
        if action == None:
            return False

        row = action // self.column_count
        column = action % self.column_count
        player = state[row, column]

        return (
                np.sum(state[row, :]) == player * self.column_count
                or np.sum(state[:, column]) == player * self.row_count
                or np.sum(np.diag(state)) == player * self.row_count
                or np.sum(np.diag(np.flip(state, axis=0))) == player * self.row_count
        )
    
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0


    def get_terminal_flags(self, state, print_flag=False):

        #3 repeated states rule
        if state.repeated_moves_flags & 0b10 > 0:
            return True
        if state.no_progress_flags >= 50:
            return True
    

        num_empty_squares = state.type_at_each_square.count(-1)

        #case 1: two kings
        if num_empty_squares == 62:
            return True
        #case 2: king bishop
        if num_empty_squares == 61 and ((state.pieces[WHITE_BISHOP].bitboard | state.pieces[BLACK_BISHOP].bitboard) > 0):
            return True
        #case 3: king knight
        if num_empty_squares == 61 and ((state.pieces[WHITE_KNIGHT].bitboard | state.pieces[BLACK_KNIGHT].bitboard) > 0):
            return True
        #case 4: king and same color bishops
        if num_empty_squares == 60 and state.pieces[WHITE_BISHOP].bitboard > 0 and state.pieces[BLACK_BISHOP].bitboard > 0:

            #checking same color
            white_square_mask = 0xaa55aa55aa55aa55
            black_square_mask = Bitboard.complement(white_square_mask)

            if ((white_square_mask | state.pieces[WHITE_BISHOP].bitboard) > 0 and (white_square_mask | state.pieces[BLACK_BISHOP].bitboard) > 0) or (((black_square_mask | state.pieces[WHITE_BISHOP].bitboard) > 0 and (black_square_mask | state.pieces[BLACK_BISHOP].bitboard) > 0)):
                return True



        return False
    





    # I don't understand what the "get_value" here does. It's 1 if the action the player plays wins and 0 otherwise? Why is it tied to the "get_terminated" "function"
    # TODO: See check_win. Have a lot of thoughts on this one. Leddon and Zach to work closely on.
    def get_value_and_terminated(self, state, action):

        #flip to black's POV
        state = self.change_perspective(state)

        black_moves = self.get_valid_moves(state)

        #flip back to white
        state = self.change_perspective(state)

        #check if black has moves (aka non-zero values in np array)
        if not np.all(black_moves == 0):

            #check the three tie flags
            if self.get_terminal_flags(state, True):
                return 0, True

            else:
                return 0, False


        #black has no moves
        else:

            #in check = 
            
            if self.is_in_check(state.pieces, BLACK):

                #mate: show board
                state.print_type_at_each_square()

                return 1, True

            #else = stalemate
            else:
                return 0, True



        # valid_moves = self.get_valid_moves(state)



        # if self.check_win(state, action):
        #     return 1, True
        # #TODO: not a win, but game is done 
        # #tie options: stalemate, 3 repeated positions, 50 move rule, TODO: insufficient material 
        # if np.sum(self.get_valid_moves(state)) == 0:
        #     return 0, True
        # return 0, False

    def get_opponent(self, player):
        return -player

    def get_opponent_value(self, value):
        return -value

    # The state is represented as initially all 0's, then 1's in the places where the current player has moved (when they view the board) and -1's where the opponent has played correct?
    # This function is then used to flip the perspective of the board so that the opponent can view it from their perspective right?

    #nice chatgpt code for flipping bitboard perspective
    def flip_vertical(self, bb):
        bb = ((bb & 0x00000000000000FF) << 56) | \
            ((bb & 0x000000000000FF00) << 40) | \
            ((bb & 0x0000000000FF0000) << 24) | \
            ((bb & 0x00000000FF000000) << 8)  | \
            ((bb & 0x000000FF00000000) >> 8)  | \
            ((bb & 0x0000FF0000000000) >> 24) | \
            ((bb & 0x00FF000000000000) >> 40) | \
            ((bb & 0xFF00000000000000) >> 56)
        return bb
    

    def flip_piece_type(self, piece_type):

        if piece_type == WHITE_PAWN:
            return BLACK_PAWN
        elif piece_type == BLACK_PAWN:
            return WHITE_PAWN
        elif piece_type == WHITE_KNIGHT:
            return BLACK_KNIGHT
        elif piece_type == BLACK_KNIGHT:
            return WHITE_KNIGHT
        elif piece_type == WHITE_BISHOP:
            return BLACK_BISHOP
        elif piece_type == BLACK_BISHOP:
            return WHITE_BISHOP
        elif piece_type == WHITE_ROOK:
            return BLACK_ROOK
        elif piece_type == BLACK_ROOK:
            return WHITE_ROOK
        elif piece_type == WHITE_QUEEN:
            return BLACK_QUEEN
        elif piece_type == BLACK_QUEEN:
            return WHITE_QUEEN
        elif piece_type == WHITE_KING:
            return BLACK_KING
        elif piece_type == BLACK_KING:
            return WHITE_KING
        else:
            return -1
        



    # Flip the perspective of white and black. White's bitboards become black's and vice versa, and all the repetition and other flags also switch
    def change_perspective(self, state):
        # return state * player

        #flip all the boards
        for piece_type in state.pieces:
            state.pieces[piece_type].bitboard = self.flip_vertical(state.pieces[piece_type].bitboard)

        #then, give all "white pieces" to black and vice versa
        #the idea here is that "white" is really just always the player making moves, 
        #so black's turn is really just white moving black's pieces 
        #hopefully that makes sense...
        state.pieces[WHITE_PAWN], state.pieces[BLACK_PAWN] = state.pieces[BLACK_PAWN], state.pieces[WHITE_PAWN]
        state.pieces[WHITE_ROOK], state.pieces[BLACK_ROOK] = state.pieces[BLACK_ROOK], state.pieces[WHITE_ROOK]
        state.pieces[WHITE_KNIGHT], state.pieces[BLACK_KNIGHT] = state.pieces[BLACK_KNIGHT], state.pieces[WHITE_KNIGHT]
        state.pieces[WHITE_BISHOP], state.pieces[BLACK_BISHOP] = state.pieces[BLACK_BISHOP], state.pieces[WHITE_BISHOP]
        state.pieces[WHITE_QUEEN], state.pieces[BLACK_QUEEN] = state.pieces[BLACK_QUEEN], state.pieces[WHITE_QUEEN]
        state.pieces[WHITE_KING], state.pieces[BLACK_KING] = state.pieces[BLACK_KING], state.pieces[WHITE_KING]

        for piece_type in state.pieces:
            state.pieces[piece_type].type = self.flip_piece_type(state.pieces[piece_type].type)

        #flip rows of type_at_each_square array, reassign each cell with opposite-side value
        new_type_at_each_square = []
        for i in range(8):
            row = state.type_at_each_square[i*8 : (i*8) + 8]

            #flip white-black values in each cell
            for j in range(8):
                row[j] = self.flip_piece_type(row[j])

            #insert to front (flips the row orders)
            new_type_at_each_square = row + new_type_at_each_square
        state.type_at_each_square = new_type_at_each_square



        #last, change documented color
        state.turn *= -1

        return state
    
    #shout out chat gpt
    def bitboard_to_array(self, bb):
        bits = np.unpackbits(np.array([bb], dtype='>u8').view(np.uint8))
        return bits.reshape((8, 8))

    # N × N × (M T + L)
    # Take the states in the queue and add the "L" part. Encode as stacked np array's as seen below
    def get_encoded_state(self, state):

        np_list = []

        for item in state.queue:

            pieces = item[0]
            rep_flags = item[1]

            
            for piece_type in pieces:
                np_form = self.bitboard_to_array(pieces[piece_type].bitboard)
                np_list.append(np_form)

            two_rep_moves = 0x0000000000000000
            if rep_flags & 0b01 > 0:
                two_rep_moves = 0xffffffffffffffff
            
            three_rep_moves = 0x0000000000000000
            if rep_flags & 0b10 > 0:
                three_rep_moves = 0xffffffffffffffff

            np_list.append(self.bitboard_to_array(two_rep_moves))
            np_list.append(self.bitboard_to_array(three_rep_moves))

            


        
        #add the 'L' bitboards
        #COLOR
        color_bitboard = 0xffffffffffffffff
        if state.turn == BLACK:
            color_bitboard = 0x0000000000000000
        
        #CASTLE
        white_castle_queen_side = 0x0000000000000000
        if state.castle_flags & 0b0001 > 0:
            white_castle_queen_side = 0xffffffffffffffff
        white_castle_king_side = 0x0000000000000000
        if state.castle_flags & 0b0010 > 0:
            white_castle_king_side = 0xffffffffffffffff
        black_castle_queen_side = 0x0000000000000000
        if state.castle_flags & 0b0100 > 0:
            black_castle_queen_side = 0xffffffffffffffff
        black_castle_king_side = 0x0000000000000000
        if state.castle_flags & 0b1000 > 0:
            black_castle_king_side = 0xffffffffffffffff

        #total move count
        total_move_count = np.full((8, 8), (state.total_move_flags/100))

        #no progress: the number of 1s maps to the value of no progress
        no_progress_count = np.full((8, 8), (state.no_progress_flags/50))

        L = [self.bitboard_to_array(color_bitboard), 
             self.bitboard_to_array(white_castle_queen_side), self.bitboard_to_array(white_castle_king_side),
             self.bitboard_to_array(black_castle_queen_side), self.bitboard_to_array(black_castle_king_side), 
             total_move_count, no_progress_count]
        
        np_list += L

        encoded_state = np.stack(np_list).astype(np.float32)
        return encoded_state



    # TO-DO: Another thing to remember is that we have to make a queue to store the T long history of the past states and repetitions
    # Link to paper: https://arxiv.org/pdf/1712.01815




