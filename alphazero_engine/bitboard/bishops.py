from bitboard.sliding_pieces import *

'''
bishops class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Bishops(SlidingPieces):

    def __init__(self, type, bitboard=None):
        super().__init__(type)
        
        if bitboard == None and type == WHITE_BISHOP:
            self.bitboard = 0x0000000000000024
            self.symbol = '\u265D'
        elif bitboard == None and type == BLACK_BISHOP:
            self.bitboard = 0x2400000000000000
            self.symbol = '\u2657'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces):

        return Bishops.all_bishop_moves(self.bitboard, empty_squares, enemy_pieces)




