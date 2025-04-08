from bitboard.bitboard import *
from bitboard.pieces import *

#useful enumerations
MOVES = 0
CASTLING = 1
ENPASSANT = 2


#stores game data
class InfoBitboards(Bitboard):

    def __init__(self):

        self.enpassant = 0x0

        #0 = no one in check
        #1 = white in check
        #2 = black in check
        #3 = both in check (not even possible)
        self.incheck = 0x0

        #castling rights:
        #0 = no one can castle
        #1 = white can castle LONG
        #3 = white can castle SHORT
        #7 = black can castle LONG
        #15 = black can castle SHORT
        self.castlingrights = 0x1111

    def king_in_check(self, color):

        if color == WHITE:
            self.incheck |= 0x1
        else:
            self.incheck |= 0x10

    def king_not_in_check(self, color):

        if color == WHITE:
            self.incheck &= 0x10
        else:
            self.incheck &= 0x01

    
    def is_king_in_check(self, color):

        if color == WHITE:
            return self.incheck & 0x1 > 0
        else:
            return self.incheck & 0x10 > 0
        
    def remove_castling_rights(self, color, long):
        
        if color == WHITE and long:
            self.castlingrights &= 0x1110
        elif color == WHITE and not long:
            self.castlingrights &= 0x1101
        elif color == BLACK and long:
            self.castlingrights &= 0x1011
        elif color == BLACK and not long:
            self.castlingrights &= 0x0111
        
        

    def has_castling_rights(self, color, long):

        if color == WHITE and long:
            return self.castlingrights & 0x0001 > 0
        elif color == WHITE and not long:
            return self.castlingrights & 0x0010 > 0
        elif color == BLACK and long:
            return self.castlingrights & 0x0100 > 0
        elif color == BLACK and not long:
            return self.castlingrights & 0x1000 > 0




    
    #functions for storing types of info

