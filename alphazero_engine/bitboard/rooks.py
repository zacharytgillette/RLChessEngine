from bitboard.sliding_pieces import *

'''
rooks class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Rooks(SlidingPieces):

    def __init__(self, type, bitboard=None):

        super().__init__(type)
        
        if bitboard == None and type == WHITE_ROOK:
            self.bitboard = 0x0000000000000081
            self.symbol = '\u265C'
        elif bitboard == None and type == BLACK_ROOK:
            self.bitboard = 0x8100000000000000
            self.symbol = '\u2656'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces):

        return Rooks.all_rook_moves(self.bitboard, empty_squares, enemy_pieces)




