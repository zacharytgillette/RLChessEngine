from bitboard.pawns import *
from bitboard.knights import *
from bitboard.kings import *
from bitboard.rooks import *
from bitboard.bishops import *
from bitboard.queens import *

import random

#create all the pieces

#white
whitePawns = Pawns(WHITE)
whiteRooks = Rooks(WHITE)
whiteKnights = Knights(WHITE)
whiteBishops = Bishops(WHITE)
whiteQueen = Queens(WHITE)
whiteKing = Kings(WHITE)

#black
blackPawns = Pawns(BLACK)
blackRooks = Rooks(BLACK)
blackKnights = Knights(BLACK)
blackBishops = Bishops(BLACK)
blackQueen = Queens(BLACK)
blackKing = Kings(BLACK)

whitePieces = [whitePawns, whiteRooks, whiteKnights, whiteBishops, whiteQueen, whiteKing]
blackPieces = [blackPawns, blackRooks, blackKnights, blackBishops, blackQueen, blackKing]


#get piece's string representation
def add_piece_symbols(current_string, bitboard, symbol):

    s = Bitboard.to_string(bitboard)

    to_ret = ""

    for i in range(64):

        if s[i] == "1":
                
            to_ret += symbol

        else:
            to_ret += current_string[i]

    return to_ret

#simple visualize
def visualize(all_pieces, old_index, new_index):



    s = "." * 64

    for pieces in all_pieces:

        s = add_piece_symbols(s, pieces.bitboard, pieces.symbol)


    to_ret = "\n"
    for i in range(8):

        for j in range(8):

            ind = i*8 + j

            to_add = s[ind] + " "

            if ind == 63-old_index:
                print("\033[91m" + to_add + "\033[0m", end="")
            elif ind == 63-new_index:
                print("\033[92m" + to_add + "\033[0m", end="")
            else:
                print(to_add, end="")

            #to_ret += to_add

        #to_ret += '\n'
        print("")

    # print(to_ret)

def get_white_bitboard(all_pieces):

    b = 0x0

    for pieces in all_pieces:

        if pieces.color == WHITE:
            b |= pieces.bitboard

    return b

def get_black_bitboard(all_pieces):

    b = 0x0

    for pieces in all_pieces:

        if pieces.color == BLACK:
            b |= pieces.bitboard

    return b

def get_all_bitboard(all_pieces):

    b = 0x0

    for pieces in all_pieces:
        b |= pieces.bitboard

    return b

def get_empty_squares(all_pieces):

    return Bitboard.complement(get_white_bitboard(all_pieces) | get_black_bitboard(all_pieces))



turn = WHITE

all_pieces = whitePieces + blackPieces
visualize(all_pieces, 99, 99)

import time

sleep_length = 1

for i in range(1000):

    #for visualization
    time.sleep(sleep_length)
    if i % 25 == 0:
        sleep_length = max(0.25, sleep_length-1)

    #save for coloring later
    old_bitboard = get_all_bitboard(all_pieces)

    #get all the moves
    all_moves = []

    if turn == WHITE:
        for pieces in whitePieces:
            moves = pieces.all_moves(get_empty_squares(all_pieces), get_black_bitboard(blackPieces))
            
            for move in moves:
                all_moves.append([move, pieces])

    elif turn == BLACK:
        for pieces in blackPieces:
            moves = pieces.all_moves(get_empty_squares(all_pieces), get_white_bitboard(whitePieces))
            for move in moves:
                all_moves.append([move, pieces])

            
    #pick random move
    ind = random.randint(0, max(len(all_moves)-1, 0))
    rand_move = all_moves[ind][0]
    pieces_type = all_moves[ind][1].type


    if turn == WHITE:

        #loop through each piece type
        for i in range(6):

            pieces = whitePieces[i]

            # see if the type of piece from the move matches
            if pieces.type == pieces_type:

                #update the official board
                whitePieces[i].bitboard = rand_move

    elif turn == BLACK:

        #loop through each piece type
        for i in range(6):

            pieces = blackPieces[i]

            # see if the type of piece from the move matches
            if pieces.type == pieces_type:

                #update the official board
                blackPieces[i].bitboard = rand_move


    #check if captures

    captures = get_white_bitboard(whitePieces) & get_black_bitboard(blackPieces)

    uncaptured = Bitboard.complement(captures)

    if turn == WHITE:

        # & uncaptures with all bitboards
        for i in range(6):
            blackPieces[i].bitboard &= uncaptured

    else:
        # & uncaptures with all bitboards
        for i in range(6):
            whitePieces[i].bitboard &= uncaptured


    #check for checks


    all_pieces = whitePieces + blackPieces

    new_bitboard = get_all_bitboard(all_pieces)
    diff = old_bitboard ^ new_bitboard

    old_piece = diff & old_bitboard
    new_piece = diff & new_bitboard

    if captures > 0:
        new_piece = captures

    old_index = SlidingPieces.get_index(old_piece)
    new_index = SlidingPieces.get_index(new_piece)

    
        

    # Bitboard.print(old_bitboard, "old")
    # Bitboard.print(new_bitboard, "new")
    # Bitboard.print(diff, "xor")

    print()
    visualize(all_pieces, old_index, new_index)

    #change color turn
    if turn == WHITE:
        turn = BLACK
    else:
        turn = WHITE

    

    #check game end
    for pieces in all_pieces:

        if pieces.type == KING:

            if pieces.bitboard == 0:

                print(str(pieces.color) + " loses")
                quit()




# board = 0x0

# for pieces in all_pieces:

#     board |= pieces.bitboard

# Bitboard.print(board)