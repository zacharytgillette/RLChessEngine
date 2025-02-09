from bitboard.simple_pieces import *

'''
pawns class: overrides functionality from simple_pieces class
'''

#useful bitboards

#second and seventh rank: useful for pawn double moves
SECOND_RANK = 0x000000000000ff00
SEVENTH_RANK = 0x00ff000000000000

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
    def get_single_moves(self, empty_squares):

        if self.color == WHITE:
            return (self.bitboard << 8) & empty_squares
        else:
            return (self.bitboard >> 8) & empty_squares
        
    #double move
    def get_double_moves(self, empty_squares):

        to_ret = None

        if self.color == WHITE:

            # valid pawns must be on second rank
            on_second_rank = self.bitboard & SECOND_RANK

            # they must be able to make one step without landing on piece
            first_move = (on_second_rank << 8) & empty_squares

            # they must be able to make the second move too
            to_ret = (first_move << 8) & empty_squares

        else:

            # valid pawns must be on seventh rank
            on_seventh_rank = self.bitboard & SEVENTH_RANK

            # they must be able to make one step without landing on piece
            first_move = (on_seventh_rank >> 8) & empty_squares

            # they must be able to make the second move too
            to_ret = (first_move >> 8) & empty_squares

        return to_ret
    

    #capture left
    def get_left_captures(self, enemy_pieces):

        if self.color == WHITE:
            return (self.bitboard << 9) & enemy_pieces
        else:
            return (self.bitboard >> 7) & enemy_pieces
    
    #capture right
    def get_right_captures(self, enemy_pieces):
        
        if self.color == WHITE:
            return (self.bitboard << 7) & enemy_pieces
        else:
            return (self.bitboard >> 9) & enemy_pieces
        
    #en passant 
    #(this requires having our meta data bitboards set up to see previous move)
    #so leave this for later
    def get_en_passant(self):
        pass
    


        
        

        

