from bitboard.bitboard import *

'''
includes basic bitboard functions relevant to all 6 piece types

includes enumerations for colors and pieces
'''
WHITE = 1
BLACK = -1

#NEW ENUMERATION TYPES
WHITE_PAWN = 0
WHITE_KNIGHT = 1
WHITE_BISHOP = 2
WHITE_ROOK = 3
WHITE_QUEEN = 4
WHITE_KING = 5
BLACK_PAWN = 6
BLACK_KNIGHT = 7
BLACK_BISHOP = 8
BLACK_ROOK = 9
BLACK_QUEEN = 10
BLACK_KING = 11


class Pieces(Bitboard):

    def __init__(self, type):
        
        self.type = type
        self.symbol = ""
        self.mark = False
        

    def move(self):
        print("No not use this; use overridden piece-specific move.")

    def print_piece_type(self, piece_type):
        if piece_type == WHITE_PAWN:
            print("WHITE PAWN")
        elif piece_type == WHITE_KNIGHT:
            print("WHITE KNIGHT")
        elif piece_type == WHITE_BISHOP:
            print("WHITE BISHOP")
        elif piece_type == WHITE_ROOK:
            print("WHITE ROOK")
        elif piece_type == WHITE_QUEEN:
            print("WHITE QUEEN")
        elif piece_type == WHITE_KING:
            print("WHITE KING")
        elif piece_type == BLACK_PAWN:
            print("BLACK PAWN")
        elif piece_type == BLACK_KNIGHT:
            print("BLACK KNIGHT")
        elif piece_type == BLACK_BISHOP:
            print("BLACK BISHOP")
        elif piece_type == BLACK_ROOK:
            print("BLACK ROOK")
        elif piece_type == BLACK_QUEEN:
            print("BLACK QUEEN")
        elif piece_type == BLACK_KING:
            print("BLACK KING")
        else:
            print("Unknown piece type")


    #add other generic piece functions here...

