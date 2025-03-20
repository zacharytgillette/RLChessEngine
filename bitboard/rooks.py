from bitboard.sliding_pieces import *

'''
rooks class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Rooks(SlidingPieces):

    def __init__(self, color, bitboard=None):
        super().__init__(ROOK, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x0000000000000081
            self.symbol = '\u265C'
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x8100000000000000
            self.symbol = '\u2656'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces, info_bitboard):

        return Rooks.all_rook_moves(self.bitboard, empty_squares, enemy_pieces, info_bitboard)




