from bitboard.pawns import *
from bitboard.knights import *
from bitboard.kings import *
from bitboard.rooks import *
from bitboard.bishops import *
from bitboard.queens import *
from bitboard.info import *

import time
import random
import copy

class Game():

    def __init__(self):

        #create all the pieces

        #white
        whitePawns = Pawns(WHITE)
        whiteRooks = Rooks(WHITE)
        whiteKnights = Knights(WHITE)
        whiteBishops = Bishops(WHITE)
        whiteQueens = Queens(WHITE)
        whiteKing = Kings(WHITE)

        #black
        blackPawns = Pawns(BLACK)
        blackRooks = Rooks(BLACK)
        blackKnights = Knights(BLACK)
        blackBishops = Bishops(BLACK)
        blackQueens = Queens(BLACK)
        blackKing = Kings(BLACK)

        self.whitePieces = {PAWN : whitePawns, 
                            ROOK : whiteRooks, 
                            KNIGHT : whiteKnights,
                            BISHOP : whiteBishops,
                            QUEEN : whiteQueens,
                            KING : whiteKing}
    
        self.blackPieces = {PAWN : blackPawns, 
                            ROOK : blackRooks, 
                            KNIGHT : blackKnights,
                            BISHOP : blackBishops,
                            QUEEN : blackQueens,
                            KING : blackKing}


        self.allPieces = list(self.whitePieces.values()) + list(self.blackPieces.values())

        #bitboards that store info
        self.infoBitboards = InfoBitboards()

        #first bit is white in check, second bit is black in check
        # self.moveRestrictions = InfoBitboard(0x0, MOVES)
        # #1 = CAN, 0 = CANT: first bit white kingside, 2nd white queenside, 3rd black kingside, 4th black queenside
        # self.castlingRights = InfoBitboard(0x1111, CASTLING)
        # #bit on square where enpassant can occur
        # self.enPassantRights = InfoBitboard(0x0, ENPASSANT)


        #game info
        self.turn = WHITE
        # self.whiteInCheck = False
        # self.blackInCheck = False

    def copy(self):
        return copy.deepcopy(self)


    def get_white_bitboard(self):

        b = 0x0
        for pieces in self.whitePieces.values():
            if pieces.color == WHITE:
                b |= pieces.bitboard
        return b

    def get_black_bitboard(self):

        b = 0x0
        for pieces in self.blackPieces.values():
            if pieces.color == BLACK:
                b |= pieces.bitboard
        return b

    def get_all_bitboard(self):

        b = 0x0
        for pieces in self.allPieces:
            b |= pieces.bitboard
        return b

    def get_empty_squares(self):
        return Bitboard.complement(self.get_white_bitboard() | self.get_black_bitboard())
    
    #simple visualiztion for terminal
    def add_piece_symbols(self, current_string, bitboard, symbol):

        s = Bitboard.to_string(bitboard)
        to_ret = ""

        for i in range(64):
            if s[i] == "1":
                to_ret += symbol
            else:
                to_ret += current_string[i]

        return to_ret

    #simple visualize
    def simple_visualize(self, old_index, new_index):

        s = "." * 64
        for pieces in self.allPieces:
            s = self.add_piece_symbols(s, pieces.bitboard, pieces.symbol)

        print("")
        for i in range(8):

            for j in range(8):

                ind = i*8 + j

                to_add = s[ind] + " "

                if ind == 63-old_index:
                    print("\033[91m" + to_add + "\033[0m", end="")
                elif ind == 63-new_index:
                    print("\033[92m" + to_add + "\033[0m", end="")
                else:
                    print(to_add, end="")

            print("")


    def get_moves(self):

        all_moves = []

        if self.turn == WHITE:
            for pieces in self.whitePieces.values():
                moves = pieces.all_moves(self.get_empty_squares(), self.get_black_bitboard(), self.infoBitboards)
                
                for move in moves:
                    all_moves.append([move, pieces])

        elif self.turn == BLACK:
            for pieces in self.blackPieces.values():
                moves = pieces.all_moves(self.get_empty_squares(), self.get_white_bitboard(), self.infoBitboards)
                for move in moves:
                    all_moves.append([move, pieces])

        return all_moves
     


    def update_game_move(self, move):

        random_move = move[0]
        pieces_type = move[1].type

        #make a copy of current game to edit
        game_copy = self.copy()

        #update bitboards with move
        if game_copy.turn == WHITE:
            game_copy.whitePieces[pieces_type].bitboard = random_move
        else:
            game_copy.blackPieces[pieces_type].bitboard = random_move


        #check if captures
        captures = game_copy.get_white_bitboard() & game_copy.get_black_bitboard()
        uncaptured = Bitboard.complement(captures)

        #update captures
        if game_copy.turn == WHITE:
            for type in game_copy.blackPieces:
                game_copy.blackPieces[type].bitboard &= uncaptured
        else:
            for type in game_copy.whitePieces:
                game_copy.whitePieces[type].bitboard &= uncaptured

        game_copy.all_pieces = list(game_copy.whitePieces.values()) + list(game_copy.blackPieces.values())

        if game_copy.turn == WHITE:
            game_copy.turn = BLACK
        else:
            game_copy.turn = WHITE

        return game_copy
    


    def is_in_check(self, color_to_capture):
        # Determine the king and temporarily switch turn
        if color_to_capture == WHITE:
            king = self.whitePieces[KING].bitboard
            opposing_color = BLACK
        elif color_to_capture == BLACK: 
            king = self.blackPieces[KING].bitboard
            opposing_color = WHITE
        else:
            raise ValueError("Invalid color specified")

        # Store the original turn
        saved_turn = self.turn
        self.turn = opposing_color

        # Get all possible moves for the opposing color
        all_moves = self.get_moves()

        # Check if ANY move results in the king being captured
        is_check = any(move[0] & king > 0 for move in all_moves)

        # Restore the original turn
        self.turn = saved_turn

        return is_check

    def is_legal_move(self, move):
        """
        Check if a move is legal by ensuring it does not put the moving player's own king in check
        
        Args:
        move: A tuple/list containing [new_bitboard, piece_to_move]
        
        Returns:
        Boolean indicating whether the move is legal
        """
        # Create a copy of the game state
        game_copy = self.copy()
        
        # Determine the current player's color
        current_color = self.turn
        
        # Apply the move to the game copy
        random_move = move[0]
        pieces_type = move[1].type
        
        # Update the piece's bitboard
        if current_color == WHITE:
            game_copy.whitePieces[pieces_type].bitboard = random_move
        else:
            game_copy.blackPieces[pieces_type].bitboard = random_move
        
        # Update captures and game state
        captures = game_copy.get_white_bitboard() & game_copy.get_black_bitboard()
        uncaptured = Bitboard.complement(captures)
        
        # Remove captured pieces
        if current_color == WHITE:
            for type in game_copy.blackPieces:
                game_copy.blackPieces[type].bitboard &= uncaptured
        else:
            for type in game_copy.whitePieces:
                game_copy.whitePieces[type].bitboard &= uncaptured
        
        # Update piece lists
        game_copy.all_pieces = list(game_copy.whitePieces.values()) + list(game_copy.blackPieces.values())
        
        # Switch turns
        game_copy.turn = BLACK if current_color == WHITE else WHITE
        
        # Check if the move puts the current player's king in check
        return not game_copy.is_in_check(current_color)

    def get_legal_moves(self):
        """
        Get all legal moves that do not put the player's own king in check
        
        Returns:
        List of legal moves
        """
        # Get all potential moves
        all_moves = self.get_moves()
        
        # Filter out illegal moves
        legal_moves = [
            move for move in all_moves 
            if self.is_legal_move(move)
        ]
        
        return legal_moves
    


    #very basic move evaluation function (just for demo purposes)
    def get_move_via_basic_evaluation(self, legal_moves):


        pieceValues = {
            PAWN : 1, 
            KNIGHT : 3,
            BISHOP : 3,
            KING : 1,
            ROOK : 5,
            QUEEN : 9
        }

        squareValues = {
            0 : -0.5,
            1 : -0.4,
            2 : -0.4,
            3 : -0.4,
            4 : -0.4,
            5 : -0.4,
            6 : -0.4,
            7 : -0.5,

            8 : -0.4,
            9 : -0.2,
            10 : 0,
            11 : 0,
            12 : 0,
            13 : 0,
            14 : -0.2,
            15 : -0.4,

            16 : -0.4,
            17 : 0,
            18 : 0.1,
            19 : 0.2,
            20 : 0.2,
            21 : 0.1,
            22 : 0,
            23 : -0.4,

            24 : -0.4,
            25 : 0,
            26 : 0.2,
            27 : 0.25,
            28 : 0.25,
            29 : 0.2,
            30 : 0,
            31 : -0.4,

            32 : -0.4,
            33 : 0,
            34 : 0.2,
            35 : 0.25,
            36 : 0.25,
            37 : 0.2,
            38 : 0,
            39 : -0.4,

            40 : -0.4,
            41 : 0,
            42 : 0.1,
            43 : 0.2,
            44 : 0.2,
            45 : 0.1,
            46 : 0,
            47 : -0.4,

            48 : -0.4,
            49 : -0.2,
            50 : 0,
            51 : 0,
            52 : 0,
            53 : 0,
            54 : -0.2,
            55 : -0.4,

            56 : -0.5,
            57 : -0.4,
            58 : -0.4,
            59 : -0.4,
            60 : -0.4,
            61 : -0.4,
            62 : -0.4,
            63 : -0.5,
        }


        #assume white, negate later if black

        best_move = None
        best_score = None

        for move in legal_moves:

            next_game_state = self.update_game_move(move)

            score = 0

            #evaluate state
            for type in next_game_state.whitePieces:

                b = next_game_state.whitePieces[type].bitboard

                b_string = Bitboard.to_string(b)

                for i in range(64):

                    c = b_string[63-i]

                    if c == '1':
                        score += pieceValues[type] * squareValues[i]

            for type in next_game_state.blackPieces:

                b = next_game_state.blackPieces[type].bitboard

                b_string = Bitboard.to_string(b)

                for i in range(64):

                    c = b_string[63-i]

                    if c == '1':
                        score -= pieceValues[type] * squareValues[i]


            if self.turn == WHITE and (best_score == None or score > best_score):
                best_score = score
                best_move = move

            elif self.turn == BLACK and (best_score == None or score < best_score):
                best_score = score
                best_move = move

        return best_move


    def update_info_bitboard(self, chosen_move, next_game_state):

        #update en passant rights
        if chosen_move[1].type == PAWN:

            original_pawn_bitboard = None

            if self.turn == WHITE:
                original_pawn_bitboard = self.whitePieces[PAWN].bitboard
            else:
                original_pawn_bitboard = self.blackPieces[PAWN].bitboard

            #xor with current board to find the jump
            diff = original_pawn_bitboard ^ chosen_move[0]
            original_pawn_bitboard = diff & original_pawn_bitboard
            new_pawn_bitboard = diff & chosen_move[0]

            #valid for en passant if double move
            if self.turn == WHITE and (new_pawn_bitboard >> 16) - original_pawn_bitboard == 0:
                next_game_state.infoBitboards.enPassantRights.bitboard = new_pawn_bitboard
            elif self.turn == BLACK and (new_pawn_bitboard << 16) - original_pawn_bitboard == 0:
                next_game_state.infoBitboards.enPassantRights.bitboard = new_pawn_bitboard
            else:
                next_game_state.infoBitboards.enPassantRights.bitboard = 0x0

        else:
            next_game_state.infoBitboards.enPassantRights.bitboard = 0x0

        return next_game_state




    def make_move(self):
        # Get legal moves
        legal_moves = self.get_legal_moves()
        
        # Check for checkmate or stalemate
        if not legal_moves:
            # Determine if it's checkmate or stalemate
            if self.is_in_check(self.turn):
                # Checkmate
                if self.turn == WHITE:
                    print("CHECKMATE: BLACK WINS")
                    return 2
                else:
                    print("CHECKMATE: WHITE WINS")
                    return 1
            else:
                # Stalemate
                print("STALEMATE")
                return -1
            
            
        # Pick a random legal move
        random.shuffle(legal_moves)
        random_move = legal_moves[0]
        chosen_move = self.get_move_via_basic_evaluation(legal_moves)

        #odds random move is picked (out of 100)
        odds = 30
        if random.randint(0, 100) < odds:
            chosen_move = random_move
        
        # Update game state with the chosen move
        next_game_state = self.update_game_move(chosen_move)

        # update info bitboard (this must come before state is updated, so we can access previous state too)
        next_game_state = self.update_info_bitboard(chosen_move, next_game_state)
        

        # Update the current game state
        self.__dict__ = next_game_state.__dict__.copy()

 
        # Check if the move puts the opponent in check
        if self.is_in_check(self.turn):
            if self.turn == WHITE:
                # self.whiteInCheck = True
                self.infoBitboards.checkInfo.bitboard |= 0x01
                print("WHITE IN CHECK")
            else:
                # self.blackInCheck = True
                self.infoBitboards.checkInfo.bitboard |= 0x10
                print("BLACK IN CHECK")
        else:
            # self.whiteInCheck = False
            # self.blackInCheck = False
            self.infoBitboards.checkInfo.bitboard &= 0x00
        
        return 0


        
    def simulate_game(self):

        #begin with default visualization
        self.simple_visualize(99, 99)

        sleep_length = 1
        for i in range(1000):

            #sleep for visualization
            time.sleep(sleep_length)
            if i % 12 == 0:
                sleep_length = max(0.25, sleep_length-1)

            #save for coloring later
            old_bitboard = self.get_all_bitboard()

            #make move
            result = self.make_move()


            #compare old and new bitboards for visualization
            new_bitboard = self.get_all_bitboard()
            diff = old_bitboard ^ new_bitboard
            old_piece = diff & old_bitboard
            new_piece = diff & new_bitboard

            captures = self.get_white_bitboard() & self.get_black_bitboard()
            # Bitboard.print(captures, "captuire")
            if captures > 0:
                # print("capture")
                new_piece = captures

            old_index = SlidingPieces.get_index(old_piece)
            new_index = SlidingPieces.get_index(new_piece)

            self.simple_visualize(old_index, new_index)

            if result == 1 or result == 2:
                return 1
            
        return 0
        


