from bitboard.pawns import *
from bitboard.kings import *
from bitboard.knights import *

def main():

    other_blockers = Bitboard(0x0000000000000000)
    #bitboard.print(sample_blockers.bitboard, "blockers")

    white_pawns = Pawns(WHITE)
    black_pawns = Pawns(BLACK)
    
    white_knights = Knights(WHITE)
    black_knights = Knights(BLACK)

    white_king = Kings(WHITE)
    black_king = Kings(BLACK)

    all_pieces = other_blockers.bitboard | white_pawns.bitboard | black_pawns.bitboard | white_knights.bitboard | black_knights.bitboard | white_king.bitboard | black_king.bitboard

    Bitboard.print(all_pieces)

    empty_squares = Bitboard.complement(all_pieces)
    enemy_pieces = black_king.bitboard | black_pawns.bitboard | black_knights.bitboard
    
    all_moves = white_knights.all_moves(empty_squares, enemy_pieces) + white_pawns.all_moves(empty_squares, enemy_pieces) + white_king.all_moves(empty_squares, enemy_pieces)

    for move in all_moves:

        Bitboard.print(move, "all da moves")



if __name__ == "__main__":
    main()