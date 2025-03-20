from bitboard.bitboard import *

'''
includes basic bitboard functions relevant to all 6 piece types

includes enumerations for pieces
'''

#color enumeration
WHITE = 0
BLACK = 1

#piece type enumeration
PAWN = 0
ROOK = 1
KNIGHT = 2
BISHOP = 3
QUEEN = 4
KING = 5



class Pieces(Bitboard):

    def __init__(self, type, color):
        
        self.type = type
        self.color = color
        self.symbol = ""
        self.mark = False
        

    def move(self):
        print("No not use this; use overridden piece-specific move.")

    #add other generic piece functions here...

