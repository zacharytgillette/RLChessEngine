from bitboard.pawns import *
from bitboard.knights import *
from bitboard.kings import *
from bitboard.rooks import *
from bitboard.bishops import *
from bitboard.queens import *
from visualize.pygame_visualizer import *
from visualize.terminal_visualizer import *
from collections import deque



class State:

          
    def __init__(self, T, other_state=None):

        #COPY CONSTRUCTOR
        if other_state != None:
            self.turn = other_state.turn
            self.T = other_state.T
            self.pieces_deep_copy(other_state.pieces)   
            self.type_at_each_square_deep_copy(other_state.type_at_each_square)    
            self.repeated_moves_deep_copy(other_state.repeated_moves)   

            #queue
            self.queue_deep_copy(other_state.queue)   

            #flags
            self.castle_flags = other_state.castle_flags
            self.en_passant_flags = other_state.en_passant_flags
            self.repeated_moves_flags = other_state.repeated_moves_flags
            self.total_move_flags = other_state.total_move_flags
            self.no_progress_flags = other_state.no_progress_flags
            self.no_progress_color_flags = other_state.no_progress_color_flags
            self.visualizer = other_state.visualizer

        #DEFAULT CONSTRUCTOR  
        else:

            self.turn = WHITE
            self.T = T

            self.visualizer = PygameVisualizer()

            #create all the pieces

            #white
            whitePawns = Pawns(WHITE_PAWN)
            whiteKnights = Knights(WHITE_KNIGHT)
            whiteBishops = Bishops(WHITE_BISHOP)
            whiteRooks = Rooks(WHITE_ROOK)
            whiteQueens = Queens(WHITE_QUEEN)
            whiteKing = Kings(WHITE_KING)

            #black
            blackPawns = Pawns(BLACK_PAWN)
            blackKnights = Knights(BLACK_KNIGHT)
            blackBishops = Bishops(BLACK_BISHOP)
            blackRooks = Rooks(BLACK_ROOK)
            blackQueens = Queens(BLACK_QUEEN)
            blackKing = Kings(BLACK_KING)

            self.pieces = {
                WHITE_PAWN : whitePawns,
                WHITE_KNIGHT : whiteKnights,
                WHITE_BISHOP : whiteBishops,
                WHITE_ROOK : whiteRooks, 
                WHITE_QUEEN : whiteQueens,
                WHITE_KING : whiteKing,

                BLACK_PAWN : blackPawns,
                BLACK_KNIGHT : blackKnights,
                BLACK_BISHOP : blackBishops,
                BLACK_ROOK : blackRooks,
                BLACK_QUEEN : blackQueens,
                BLACK_KING : blackKing
            }

            #piece at each square
            self.type_at_each_square = [
                WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK,
                WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, 
                -1, -1, -1, -1, -1, -1, -1, -1, 
                -1, -1, -1, -1, -1, -1, -1, -1, 
                -1, -1, -1, -1, -1, -1, -1, -1, 
                -1, -1, -1, -1, -1, -1, -1, -1, 
                BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, 
                BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK,
               
            ]


            self.repeated_moves = {}
            



            #FLAGS
            
            #castle flag: 0th: white-queen, 1st: white-king, 2nd: black-queen, 3rd: black-king
            self.castle_flags = 0b1111
            #en passant: if a pawn COULD be en-passaned, it goes here
            self.en_passant_flags = 0b0
            #repeated moves: 0th bit ON if this is second time seeing state, 1st bit on if third time seeing state
            self.repeated_moves_flags = 0b0
            #total moves: just increment by 1 after black moves
            self.total_move_flags = 0b0
            #no progress: number of moves since either 1. pawn moved OR 2. piece captured
            self.no_progress_flags = 0b0
            self.no_progress_color_flags = -1

            #queue: store [self.pieces, self.repeated_moves_flags]
            self.queue = deque()

            for i in range(self.T):

                self.queue.append([self.pieces, self.repeated_moves_flags])

           
    '''
    DEEP COPY FUNCTIONS
    '''
    #overloaded
    def pieces_deep_copy_other(other_state_pieces):

        #TODO: OPTIMIZATION REVISIT

        whitePawns = Pawns(WHITE_PAWN)
        whiteKnights = Knights(WHITE_KNIGHT)
        whiteBishops = Bishops(WHITE_BISHOP)
        whiteRooks = Rooks(WHITE_ROOK)
        whiteQueens = Queens(WHITE_QUEEN)
        whiteKing = Kings(WHITE_KING)

        #black
        blackPawns = Pawns(BLACK_PAWN)
        blackKnights = Knights(BLACK_KNIGHT)
        blackBishops = Bishops(BLACK_BISHOP)
        blackRooks = Rooks(BLACK_ROOK)
        blackQueens = Queens(BLACK_QUEEN)
        blackKing = Kings(BLACK_KING)

        pieces = {
            WHITE_PAWN : whitePawns,
            WHITE_KNIGHT : whiteKnights,
            WHITE_BISHOP : whiteBishops,
            WHITE_ROOK : whiteRooks, 
            WHITE_QUEEN : whiteQueens,
            WHITE_KING : whiteKing,

            BLACK_PAWN : blackPawns,
            BLACK_KNIGHT : blackKnights,
            BLACK_BISHOP : blackBishops,
            BLACK_ROOK : blackRooks,
            BLACK_QUEEN : blackQueens,
            BLACK_KING : blackKing
        }

        for piece_type in other_state_pieces:
            pieces[piece_type].bitboard = other_state_pieces[piece_type].bitboard

        return pieces

    def pieces_deep_copy(self, other_state_pieces):

        #TODO: OPTIMIZATION REVISIT

        whitePawns = Pawns(WHITE_PAWN)
        whiteKnights = Knights(WHITE_KNIGHT)
        whiteBishops = Bishops(WHITE_BISHOP)
        whiteRooks = Rooks(WHITE_ROOK)
        whiteQueens = Queens(WHITE_QUEEN)
        whiteKing = Kings(WHITE_KING)

        #black
        blackPawns = Pawns(BLACK_PAWN)
        blackKnights = Knights(BLACK_KNIGHT)
        blackBishops = Bishops(BLACK_BISHOP)
        blackRooks = Rooks(BLACK_ROOK)
        blackQueens = Queens(BLACK_QUEEN)
        blackKing = Kings(BLACK_KING)

        self.pieces = {
            WHITE_PAWN : whitePawns,
            WHITE_KNIGHT : whiteKnights,
            WHITE_BISHOP : whiteBishops,
            WHITE_ROOK : whiteRooks, 
            WHITE_QUEEN : whiteQueens,
            WHITE_KING : whiteKing,

            BLACK_PAWN : blackPawns,
            BLACK_KNIGHT : blackKnights,
            BLACK_BISHOP : blackBishops,
            BLACK_ROOK : blackRooks,
            BLACK_QUEEN : blackQueens,
            BLACK_KING : blackKing
        }

        for piece_type in other_state_pieces:
            self.pieces[piece_type].bitboard = other_state_pieces[piece_type].bitboard

    def type_at_each_square_deep_copy(self, other_state_type_at_each_square):

        self.type_at_each_square = []

        for i in range(64):
            self.type_at_each_square.append(other_state_type_at_each_square[i])


    def repeated_moves_deep_copy(self, other_state_repeated_moves):

        self.repeated_moves = {}
        for key in other_state_repeated_moves:
            self.repeated_moves[key] = other_state_repeated_moves[key]

    
    def queue_deep_copy(self, other_state_queue):

        self.queue = deque()

        # Chatgpt recommends for time complexity
        other_state_queue_list = list(other_state_queue)

        for i in range(len(other_state_queue_list)):

            #create deep copy of queue contents
            pieces = State.pieces_deep_copy_other(other_state_queue_list[i][0])
            repeated_moves = other_state_queue_list[i][1]
            
            self.queue.append([pieces, repeated_moves])



    '''
    PRINTING FUNCTIONS (debugging)
    '''
    def print_pieces_from_bitboard(pieces):

        int_to_cha = {
            -1 : ".",

            WHITE_PAWN : "P",
            WHITE_KNIGHT : "N",
            WHITE_BISHOP : "B",
            WHITE_ROOK : "R",
            WHITE_QUEEN : "Q",
            WHITE_KING : "K",

            BLACK_PAWN : "p",
            BLACK_KNIGHT : "n",
            BLACK_BISHOP : "b",
            BLACK_ROOK : "r",
            BLACK_QUEEN : "q",
            BLACK_KING : "k"
        }

        to_print = [-1] * 64

        for piece_type in pieces:

            s = Bitboard.to_string(pieces[piece_type].bitboard)


            for i in range(64):

                if s[i] == "1":
                    to_print[63-i] = piece_type

        
        #print
        to_ret = ""

        for i in range(8):

            row = ""

            for j in range(8):

                ind = (i*8) + j

                cha = int_to_cha[to_print[ind]]
                
                if len(cha) == 1:
                    cha = " " + cha

                row = cha + " " + row

            to_ret = row + '\n' + to_ret

        print(to_ret)




            




    def print_type_at_each_square(self):

        int_to_cha = {
            -1 : ".",

            WHITE_PAWN : "P",
            WHITE_KNIGHT : "N",
            WHITE_BISHOP : "B",
            WHITE_ROOK : "R",
            WHITE_QUEEN : "Q",
            WHITE_KING : "K",

            BLACK_PAWN : "p",
            BLACK_KNIGHT : "n",
            BLACK_BISHOP : "b",
            BLACK_ROOK : "r",
            BLACK_QUEEN : "q",
            BLACK_KING : "k"
        }

        to_ret = ""

        for i in range(8):

            row = ""

            for j in range(8):

                ind = (i*8) + j

                cha = int_to_cha[self.type_at_each_square[ind]]
                
                if len(cha) == 1:
                    cha = " " + cha

                row = cha + " " + row

            to_ret = row + '\n' + to_ret

        print(to_ret)

    def get_different_squares_between_states(self, other_state):

        diff = []

        for i in range(64):
            
            if self.type_at_each_square[i] != other_state.type_at_each_square[i]:
                diff += [i]

        if len(diff) == 0:
            return [-1, -1]
        return diff
    
    def count_differences(self, other_state):

        count = 0

        for i in range(64):
            if self.type_at_each_square[i] != other_state.type_at_each_square[i]:
                count += 1

        return count

            

        
 

