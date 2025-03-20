from bitboard.bitboard import *

#useful enumerations
MOVES = 0
CASTLING = 1
ENPASSANT = 2


#stores game data
class InfoBitboards(Bitboard):

    def __init__(self):

        self.checkInfo = Bitboard(0x0)
        #1 = CAN, 0 = CANT: first bit white kingside, 2nd white queenside, 3rd black kingside, 4th black queenside
        self.castlingRights = Bitboard(0x1111)
        #bit on square where enpassant can occur
        self.enPassantRights = Bitboard(0x0)

        #message bitboard: stores responses to draw requests, pawn promotions
        #pawn promotions: knight (1) - bishop (2) - rook (3) - queen (4)
        #draw request: white (5) - black (6)
        self.message = Bitboard(0x0)


    
    #functions for storing types of info

