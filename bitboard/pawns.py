from bitboard.simple_pieces import *

'''
pawns class: overrides functionality from simple_pieces class
'''

#useful bitboards

#second and seventh rank: useful for pawn double moves
SECOND_RANK = 0x000000000000ff00
SEVENTH_RANK = 0x00ff000000000000

#empty left barrier (for pawn capture moves that wrap around the right to the left)
EMPTY_LEFT_SIDE = 0x7f7f7f7f7f7f7f7f
#empty right barrier (for pawn capture moves that wrap around the left to the right)
EMPTY_RIGHT_SIDE = 0xfefefefefefefefe

class Pawns(SimplePieces):

    def __init__(self, color, bitboard=None):
        super().__init__(PAWN, color)
        
        if bitboard == None and color == WHITE:
            self.bitboard = 0x000000000000ff00
        elif bitboard == None and color == BLACK:
            self.bitboard = 0x00ff000000000000
        else:
            self.bitboard = bitboard

    
    '''
    move generation
    '''

    #single move
    def single_moves(self, bitboard, empty_squares):

        if self.color == WHITE:
            return (bitboard << 8) & empty_squares
        else:
            return (bitboard >> 8) & empty_squares
        
    #double move
    def double_moves(self, bitboard, empty_squares):

        to_ret = None

        if self.color == WHITE:

            # valid pawns must be on second rank
            on_second_rank = bitboard & SECOND_RANK

            # they must be able to make one step without landing on piece
            first_move = (on_second_rank << 8) & empty_squares

            # they must be able to make the second move too
            to_ret = (first_move << 8) & empty_squares

        else:

            # valid pawns must be on seventh rank
            on_seventh_rank = bitboard & SEVENTH_RANK

            # they must be able to make one step without landing on piece
            first_move = (on_seventh_rank >> 8) & empty_squares

            # they must be able to make the second move too
            to_ret = (first_move >> 8) & empty_squares

        return to_ret
    

    #capture left
    def left_captures(self, bitboard, enemy_pieces):

        if self.color == WHITE:
            return (bitboard << 9) & enemy_pieces & EMPTY_RIGHT_SIDE
        else:
            return (bitboard >> 7) & enemy_pieces & EMPTY_RIGHT_SIDE
    
    #capture right
    def right_captures(self, bitboard, enemy_pieces):
        
        if self.color == WHITE:
            return (self.bitboard << 7) & enemy_pieces & EMPTY_LEFT_SIDE
        else:
            return (self.bitboard >> 9) & enemy_pieces & EMPTY_LEFT_SIDE
        
    #en passant 
    #(this requires having our meta data bitboards set up to see previous move)
    #so leave this for later
    def en_passant(self, bitboard, empty_squares, enemy_pieces):
        pass



    '''
    compute resulting bitboards
    '''

    def all_moves(self, empty_squares, enemy_pieces):

        #store all the (pre-move, post-move) mappings of individual piece bitmaps
        unique_post_move_bitboards = []

        #SINGLE MOVES
        post_move = self.single_moves(self.bitboard, empty_squares)
        while post_move:

            #get least-significant bit's bitboard of post-move bitboard
            to_square = Bitboard.get_lsb(post_move)

            #find where it came from (call opposite move function)
            if self.color == WHITE:
                from_square = to_square >> 8
            else:
                from_square = to_square << 8

            #create and store new bitboard where the specific move is reflected
            to_add = (self.bitboard | to_square) & (Bitboard.complement(from_square))
            unique_post_move_bitboards.append(to_add)

            #remove lsb from post_move bitboard so that we can repeat with next move
            post_move = Bitboard.remove_lsb(post_move, to_square)


        #DOUBLE MOVES
        post_move = self.double_moves(self.bitboard, empty_squares)
        while post_move:

            #get least-significant bit's bitboard of post-move bitboard
            to_square = Bitboard.get_lsb(post_move)

            #find where it came from (call opposite move function)
            if self.color == WHITE:
                from_square = to_square >> 16
            else:
                from_square = to_square << 16

            #create and store new bitboard where the specific move is reflected
            to_add = (self.bitboard | to_square) & (Bitboard.complement(from_square))
            unique_post_move_bitboards.append(to_add)

            #remove lsb from post_move bitboard so that we can repeat with next move
            post_move = Bitboard.remove_lsb(post_move, to_square)



        #LEFT CAPTURE
        post_move = self.left_captures(self.bitboard, enemy_pieces)
        while post_move:

            #get least-significant bit's bitboard of post-move bitboard
            to_square = Bitboard.get_lsb(post_move)

            #find where it came from (call opposite move function)
            if self.color == WHITE:
                from_square = to_square >> 9 
            else:
                from_square = to_square << 7

            #create and store new bitboard where the specific move is reflected
            to_add = (self.bitboard | to_square) & (Bitboard.complement(from_square))
            unique_post_move_bitboards.append(to_add)

            #remove lsb from post_move bitboard so that we can repeat with next move
            post_move = Bitboard.remove_lsb(post_move, to_square)



        #RIGHT CAPTURE
        post_move = self.right_captures(self.bitboard, enemy_pieces)
        while post_move:

            #get least-significant bit's bitboard of post-move bitboard
            to_square = Bitboard.get_lsb(post_move)

            #find where it came from (call opposite move function)
            if self.color == WHITE:
                from_square = to_square >> 7 
            else:
                from_square = to_square << 9

            #create and store new bitboard where the specific move is reflected
            to_add = (self.bitboard | to_square) & (Bitboard.complement(from_square))
            unique_post_move_bitboards.append(to_add)

            #remove lsb from post_move bitboard so that we can repeat with next move
            post_move = Bitboard.remove_lsb(post_move, to_square)



        return unique_post_move_bitboards
    


        
        

        

