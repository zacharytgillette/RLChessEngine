from bitboard.pawns import *
from bitboard.kings import *
from bitboard.knights import *

def main():

    sample_blockers = Bitboard(0x0000000000000000)
    #bitboard.print(sample_blockers.bitboard, "blockers")
    
    white_knights = Knights(WHITE)
    black_knights = Knights(BLACK)

    Bitboard.print(white_knights.bitboard | black_knights.bitboard)

    empty_squares = Bitboard.complement(sample_blockers.bitboard)
    
    Bitboard.print(black_knights.all_moves(empty_squares), "after")

if __name__ == "__main__":
    main()