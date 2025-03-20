from bitboard.sliding_pieces import *

'''
queens class: overrides functionality from sliding_pieces class
'''

#useful bitboards

class Queens(SlidingPieces):

    def __init__(self, color, bitboard=None):
        super().__init__(QUEEN, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x0000000000000010
            self.symbol = '\u265B'
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x1000000000000000
            self.symbol = '\u2655'
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''
    def all_moves(self, empty_squares, enemy_pieces, info_bitboard):

        return Queens.all_rook_moves(self.bitboard, empty_squares, enemy_pieces, info_bitboard) + Queens.all_bishop_moves(self.bitboard, empty_squares, enemy_pieces, info_bitboard)




