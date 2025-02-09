from bitboard.simple_pieces import *

'''
kings class: overrides functionality from simple_pieces class
'''

#useful bitboards

#empty left barrier (for king moves that wrap around the right to the left)
EMPTY_LEFT_SIDE = 0x7f7f7f7f7f7f7f7f
#empty right barrier (for king moves that wrap around the left to the right)
EMPTY_RIGHT_SIDE = 0xfefefefefefefefe

class Kings(SimplePieces):

    def __init__(self, color, bitboard=None):
        super().__init__(KING, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x0000000000000008
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x0800000000000000
        else:
            self.bitboard = bitboard


    '''
    move generation
    '''

    def all_moves(self, empty_squares):

        #left and right
        left_move = (self.bitboard << 1) & empty_squares & EMPTY_RIGHT_SIDE
        right_move = (self.bitboard >> 1) & empty_squares & EMPTY_LEFT_SIDE

        #up and down
        up_move = (self.bitboard << 8) & empty_squares
        down_move = (self.bitboard >> 8) & empty_squares

        #diagonal
        up_left_move = (self.bitboard << 9) & empty_squares & EMPTY_RIGHT_SIDE
        down_left_move = (self.bitboard >> 7) & empty_squares & EMPTY_RIGHT_SIDE
        up_right_move = (self.bitboard << 7) & empty_squares & EMPTY_LEFT_SIDE
        down_right_move = (self.bitboard >> 9) & empty_squares & EMPTY_LEFT_SIDE

        return left_move | right_move | up_move | down_move | up_left_move | down_left_move | up_right_move | down_right_move