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

        self.opposite_move_functions = {

            Kings.left: Kings.right,
            Kings.right: Kings.left,

            Kings.up: Kings.down,
            Kings.down: Kings.up,

            Kings.up_left: Kings.down_right,
            Kings.down_right: Kings.up_left,

            Kings.up_right: Kings.down_left,
            Kings.down_left: Kings.up_right,
            
        }


    '''
    move generation
    '''
    def left(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 1) & (empty_squares | enemy_pieces) & EMPTY_RIGHT_SIDE
    
    def right(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 1) & (empty_squares | enemy_pieces) & EMPTY_LEFT_SIDE
    
    def up(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 8) & (empty_squares | enemy_pieces)
    
    def down(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 8) & (empty_squares | enemy_pieces)
    
    def up_left(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 9) & (empty_squares | enemy_pieces) & EMPTY_RIGHT_SIDE
    
    def down_left(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 7) & (empty_squares | enemy_pieces) & EMPTY_RIGHT_SIDE
    
    def up_right(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard << 7) & (empty_squares | enemy_pieces) & EMPTY_LEFT_SIDE
    
    def down_right(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        return (bitboard >> 9) & (empty_squares | enemy_pieces) & EMPTY_LEFT_SIDE




    #exact same code for knights!
    def all_moves(self, empty_squares, enemy_pieces):

        #store all the (pre-move, post-move) mappings of individual piece bitmaps
        unique_post_move_bitboards = []

        #execute each of the 8 types of king moves
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