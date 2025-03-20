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
            self.symbol = '\u265E'
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x4200000000000000
            self.symbol = '\u2658'
        else:
            self.bitboard = bitboard

        self.opposite_move_functions = {

            Knights.up_left: Knights.down_right,
            Knights.up_right: Knights.down_left,
            Knights.down_left: Knights.up_right,
            Knights.down_right: Knights.up_left,

            Knights.left_up: Knights.right_down,
            Knights.left_down: Knights.right_up,
            Knights.right_up: Knights.left_down,
            Knights.right_down: Knights.left_up

        }


    '''
    move generation
    '''

    def up_left(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 17) & (empty_squares | enemy_pieces) & EMPTY_RIGHT_SIDE
    
    def up_right(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 15) & (empty_squares | enemy_pieces) & EMPTY_LEFT_SIDE
    
    def down_left(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 15) & (empty_squares | enemy_pieces) & EMPTY_RIGHT_SIDE

    def down_right(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 17) & (empty_squares | enemy_pieces) & EMPTY_LEFT_SIDE

    def left_up(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 10) & (empty_squares | enemy_pieces) & EMPTY_TWO_RIGHT_SIDE

    def left_down(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 6) & (empty_squares | enemy_pieces) & EMPTY_TWO_RIGHT_SIDE

    def right_up(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 6) & (empty_squares | enemy_pieces) & EMPTY_TWO_LEFT_SIDE

    def right_down(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 10) & (empty_squares | enemy_pieces) & EMPTY_TWO_LEFT_SIDE


    '''
    compute resulting bitboards
    '''

    def all_moves(self, empty_squares, enemy_pieces, info_bitboard):

        #store all the (pre-move, post-move) mappings of individual piece bitmaps
        unique_post_move_bitboards = []

        #execute each of the 8 types of knight moves
        for move in self.opposite_move_functions:

            #bitboard POST making the move
            post_move = move(self.bitboard, empty_squares, enemy_pieces)

            while post_move:

                #get least-significant bit's bitboard of post-move bitboard
                to_square = Bitboard.get_lsb(post_move)

                #find where it came from (call opposite move function)
                from_square = self.opposite_move_functions[move](to_square)

                #create and store new bitboard where the specific move is reflected
                to_add = (self.bitboard | to_square) & (Bitboard.complement(from_square))
                unique_post_move_bitboards.append(to_add)
                
                #remove lsb from post_move bitboard so that we can repeat with next move
                post_move = Bitboard.remove_lsb(post_move, to_square)

        return unique_post_move_bitboards

