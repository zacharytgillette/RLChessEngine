from bitboard.sliding_pieces import *

'''
bishops class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Bishops(SlidingPieces):

    def __init__(self, color, bitboard=None):
        super().__init__(BISHOP, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x0000000000000024
            self.symbol = '\u265D'
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x2400000000000000
            self.symbol = '\u2657'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces, info_bitboard):

        return Bishops.all_bishop_moves(self.bitboard, empty_squares, enemy_pieces, info_bitboard)




