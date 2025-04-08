from bitboard.sliding_pieces import *

'''
queens class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Queens(SlidingPieces):

    def __init__(self, type, bitboard=None):
        super().__init__(type)
        
        if bitboard == None and type == WHITE_QUEEN:
            self.bitboard = 0x0000000000000010
            self.symbol = '\u265B'
        elif bitboard == None and type == BLACK_QUEEN:
            self.bitboard = 0x1000000000000000
            self.symbol = '\u2655'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces):

        return Queens.all_rook_moves(self.bitboard, empty_squares, enemy_pieces) + Queens.all_bishop_moves(self.bitboard, empty_squares, enemy_pieces)




