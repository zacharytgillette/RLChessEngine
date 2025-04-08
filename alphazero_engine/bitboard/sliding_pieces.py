from bitboard.pieces import *
import math

'''
class for sliding pieces: queens, rooks, bishops
'''

'''
MASKS
'''




class SlidingPieces(Pieces):

    def __init__(self, type):
        super().__init__(type)

    '''
    MAIN FUNCTIONS (to be used by child classes)
    '''




    def get_horizontal_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):

        l_ray = SlidingPieces.get_left_horizontal_ray(bitboard, empty_squares, enemy_pieces, "LEFT")
        r_ray = SlidingPieces.get_right_horizontal_ray(bitboard, empty_squares, enemy_pieces, "RIGHT")

        return l_ray | r_ray
    
    def get_vertical_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):
        
        l_ray = SlidingPieces.get_left_horizontal_ray(SlidingPieces.flip_diagonal(bitboard), SlidingPieces.flip_diagonal(empty_squares), SlidingPieces.flip_diagonal(enemy_pieces), "UP")
        r_ray = SlidingPieces.get_right_horizontal_ray(SlidingPieces.flip_diagonal(bitboard), SlidingPieces.flip_diagonal(empty_squares), SlidingPieces.flip_diagonal(enemy_pieces), "DOWN")

        return SlidingPieces.flip_diagonal(l_ray | r_ray)
    
    
    def get_diagonal_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):

        index = SlidingPieces.get_index(bitboard)
        to_ret = 0x0

        #safety incase bitboard is empty
        if index == 99:
            return to_ret
        
        enemy_sub = Bitboard.to_string(enemy_pieces)[::-1]
        empty_sub = Bitboard.to_string(empty_squares)[::-1]

        
        #top left
        x, y = SlidingPieces.get_coors(index)
        x += 1
        y += 1
        while(x < 8 and y < 8):


            # if not empty and not taking an enemy piece, then nothing here
            if empty_sub[SlidingPieces.get_index_from_coors(x, y)] == "0" and enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "0":
                break

            ind = SlidingPieces.get_index_from_coors(x, y)
            to_ret |= (2 ** ind)

            #break if landed on another piece
            if enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "1":
                break

            x += 1
            y += 1

        #top right
        x, y = SlidingPieces.get_coors(index)
        x -= 1
        y += 1
        while(x >= 0 and y < 8):


            # if not empty and not taking an enemy piece, then nothing here
            if empty_sub[SlidingPieces.get_index_from_coors(x, y)] == "0" and enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "0":
                break

            ind = SlidingPieces.get_index_from_coors(x, y)
            to_ret |= (2 ** ind)

            #break if landed on another piece
            if enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "1":
                break

            x -= 1
            y += 1

        #bottom right
        x, y = SlidingPieces.get_coors(index)
        x -= 1
        y -= 1
        while(x >= 0 and y >= 0):


            # if not empty and not taking an enemy piece, then nothing here
            if empty_sub[SlidingPieces.get_index_from_coors(x, y)] == "0" and enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "0":
                break

            ind = SlidingPieces.get_index_from_coors(x, y)
            to_ret |= (2 ** ind)

            #break if landed on another piece
            if enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "1":
                break

            x -= 1
            y -= 1

        #bottom left
        x, y = SlidingPieces.get_coors(index)
        x += 1
        y -= 1
        while(x < 8 and y >= 0):


            # if not empty and not taking an enemy piece, then nothing here
            if empty_sub[SlidingPieces.get_index_from_coors(x, y)] == "0" and enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "0":
                break

            ind = SlidingPieces.get_index_from_coors(x, y)
            to_ret |= (2 ** ind)

            #break if landed on another piece
            if enemy_sub[SlidingPieces.get_index_from_coors(x, y)] == "1":
                break

            x += 1
            y -= 1

        return to_ret

    def all_rook_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):

        #rewritten to support many rooks, not just two

        #first, create a list of isolated rook bitboards
        rook_bb = bitboard
        isolated_rook_bbs = []

        while(rook_bb > 0):

            isolated_bb = Bitboard.get_lsb(rook_bb)

            #save it
            isolated_rook_bbs.append(isolated_bb)

            #remove it from combined bb
            rook_bb = Bitboard.remove_lsb(rook_bb, isolated_bb)

        #now, find moves for each isolated bitboard
        unique_post_move_bitboards = []
        for rook in isolated_rook_bbs:

            rook_complement = Bitboard.complement(rook)

            #verical
            vertical_moves = SlidingPieces.get_vertical_moves(rook, empty_squares, enemy_pieces & rook_complement)
            #horizontal
            horizontal_moves = SlidingPieces.get_horizontal_moves(rook, empty_squares, enemy_pieces & rook_complement)

            moves_bitboard = vertical_moves | horizontal_moves

            #bitboard without current move
            bitboard_removed_rook = bitboard & Bitboard.complement(rook)

            #save all final rook bitboards
            while(moves_bitboard > 0):

                #get single move
                isolated_move = Bitboard.get_lsb(moves_bitboard)

                #add it to bitboard of all the other rooks
                combined_rook_bb = bitboard_removed_rook | isolated_move

                #save it
                unique_post_move_bitboards.append(combined_rook_bb)

                #remove single move from moves bitboard, repeat
                moves_bitboard = Bitboard.remove_lsb(moves_bitboard, isolated_move)

        return unique_post_move_bitboards
    

    def all_bishop_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):

        #rewritten to support many BISHOPS, not just two
        #nearly identical code to rook function, so I didn't bother changing the var names

        #first, create a list of isolated rook bitboards
        rook_bb = bitboard
        isolated_rook_bbs = []

        while(rook_bb > 0):

            isolated_bb = Bitboard.get_lsb(rook_bb)

            #save it
            isolated_rook_bbs.append(isolated_bb)

            #remove it from combined bb
            rook_bb = Bitboard.remove_lsb(rook_bb, isolated_bb)

        #now, find moves for each isolated bitboard
        unique_post_move_bitboards = []
        for rook in isolated_rook_bbs:

            rook_complement = Bitboard.complement(rook)

            
            moves_bitboard = SlidingPieces.get_diagonal_moves(rook, empty_squares, enemy_pieces)

            #bitboard without current move
            bitboard_removed_rook = bitboard & Bitboard.complement(rook)

            #save all final rook bitboards
            while(moves_bitboard > 0):

                #get single move
                isolated_move = Bitboard.get_lsb(moves_bitboard)

                #add it to bitboard of all the other rooks
                combined_rook_bb = bitboard_removed_rook | isolated_move

                #save it
                unique_post_move_bitboards.append(combined_rook_bb)

                #remove single move from moves bitboard, repeat
                moves_bitboard = Bitboard.remove_lsb(moves_bitboard, isolated_move)

        return unique_post_move_bitboards
    




    '''
    HELPER FUNCTIONS
    '''

    #gets index (0-63, starting from bottom right=0) of bitboard 
    def get_index(bitboard):

        if bitboard == 0x0:
            return 99

        return int(math.log2(max(Bitboard.get_lsb(bitboard), 1)))
    
    def get_coors(index):
        return [(index % 8), index // 8]
    
    def get_index_from_coors(x, y):
        return y*8 + x
    

    def get_left_horizontal_ray(bitboard, empty_squares, enemy_pieces, debug_message=None):

        #find distance to wall
        rook_index = SlidingPieces.get_index(bitboard)
        if rook_index == 99:
            return 0x0
        dist_from_RIGHT_wall = rook_index % 8
        dist_from_LEFT_wall = 7 - dist_from_RIGHT_wall

        #find distance to closest enemy piece AFTER rook_index
        enemy_pieces_shifted = enemy_pieces >> rook_index
        dist_from_enemy = SlidingPieces.get_index(Bitboard.get_lsb(enemy_pieces_shifted)) - 1

        #find distance to closest piece on SAME team

        #find distance to closest piece (in general) AFTER rook_index                NEW CODE:
        blockers = Bitboard.complement(empty_squares) & Bitboard.complement(bitboard) & Bitboard.complement(enemy_pieces)
        blockers_shifted = blockers >> rook_index
        dist_from_blocker = SlidingPieces.get_index(Bitboard.get_lsb(blockers_shifted)) - 1

        # Bitboard.print(blockers_shifted, "blockers shifted")

        # print(debug_message)
        # print(dist_from_LEFT_wall, "left wall")
        # print(dist_from_enemy, "enemy")
        # print(dist_from_blocker, "blocker")

        limiting_reactant = int(min(dist_from_LEFT_wall, min(dist_from_enemy, dist_from_blocker)))

        #we take in the case of enemy, but not in the case of general non-enemy blocker
        #so off by one error when min is due to enemy
        if limiting_reactant == dist_from_enemy and limiting_reactant >= 0 and dist_from_blocker > limiting_reactant and dist_from_LEFT_wall > 0 and dist_from_LEFT_wall != dist_from_enemy:
            limiting_reactant += 1

        if limiting_reactant == -1:
            limiting_reactant = 0


        return  (2 ** (limiting_reactant) - 1) << (rook_index+1)





    
    def get_right_horizontal_ray(bitboard, empty_squares, enemy_pieces, debug_message=None):

        rev_bitboard = Bitboard.reverse(bitboard)
        rev_enemy_pieces = Bitboard.reverse(enemy_pieces)
        rev_empty_squares = Bitboard.reverse(empty_squares)

        rev_r_ray = SlidingPieces.get_left_horizontal_ray(rev_bitboard, rev_empty_squares, rev_enemy_pieces, debug_message)

        r_ray = Bitboard.reverse(rev_r_ray)


        return r_ray
    

    #insane clutch from chat gpt here
    def flip_diagonal(bb):
        t = 0
        k1 = 0x5500550055005500
        k2 = 0x3333000033330000
        k4 = 0x0f0f0f0f00000000

        # Stage 1
        t  = k4 & (bb ^ (bb << 28))
        bb ^=       t ^ (t >> 28)

        # Stage 2
        t  = k2 & (bb ^ (bb << 14))
        bb ^=       t ^ (t >> 14)

        # Stage 3
        t  = k1 & (bb ^ (bb << 7))
        bb ^=       t ^ (t >> 7)

        return bb
    
        








    