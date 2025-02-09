from bitboard.simple_pieces import *

'''
knights class: overrides functionality from simple_pieces class
'''

#useful bitboards

#empty left barrier (for vertical knight moves that wrap around the right to the left)
EMPTY_LEFT_SIDE = 0x7f7f7f7f7f7f7f7f
#empty right barrier (for vertical knight moves that wrap around the left to the right)
EMPTY_RIGHT_SIDE = 0xfefefefefefefefe
#empty left barrier (for horizontal knight moves that wrap around the right to the left)
EMPTY_TWO_LEFT_SIDE = 0x3f3f3f3f3f3f3f3f
#empty right barrier (for horizontal knight moves that wrap around the left to the right)
EMPTY_TWO_RIGHT_SIDE = 0xfcfcfcfcfcfcfcfc


class Knights(SimplePieces):

    def __init__(self, color, bitboard=None):
        super().__init__(KNIGHT, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x0000000000000042
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x4200000000000000
        else:
            self.bitboard = bitboard


    '''
    move generation
    '''

    def all_moves(self, empty_squares):

        #up 2 moves
        up_left = (self.bitboard << 17) & empty_squares & EMPTY_RIGHT_SIDE
        up_right = (self.bitboard << 15) & empty_squares & EMPTY_LEFT_SIDE

        #down 2 moves
        down_left = (self.bitboard >> 15) & empty_squares & EMPTY_RIGHT_SIDE
        down_right = (self.bitboard >> 17) & empty_squares & EMPTY_LEFT_SIDE

        #left 2 moves
        left_up = (self.bitboard << 10) & empty_squares & EMPTY_TWO_RIGHT_SIDE
        left_down = (self.bitboard >> 6) & empty_squares & EMPTY_TWO_RIGHT_SIDE

        #right 2 moves
        right_up = (self.bitboard << 6) & empty_squares & EMPTY_TWO_LEFT_SIDE
        right_down = (self.bitboard >> 10) & empty_squares & EMPTY_TWO_LEFT_SIDE

        return up_left | up_right | down_left | down_right | left_up | left_down | right_up | right_down