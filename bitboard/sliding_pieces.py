from bitboard.pieces import *
import math

'''
class for sliding pieces: queens, rooks, bishops
'''

'''
MASKS
'''




class SlidingPieces(Pieces):

    def __init__(self, type, color):
        super().__init__(type, color)

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


    def all_rook_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff, info_bitboard=None):

        rook1 = Bitboard.get_lsb(bitboard)
        rook2 = Bitboard.remove_lsb(bitboard, rook1)

        rook1_comp = Bitboard.complement(rook1)
        rook2_comp = Bitboard.complement(rook2)

        h1 = SlidingPieces.get_horizontal_moves(rook1, empty_squares, enemy_pieces & rook1_comp)
        v1 = SlidingPieces.get_vertical_moves(rook1, empty_squares, enemy_pieces & rook1_comp)

        h2 = SlidingPieces.get_horizontal_moves(rook2, empty_squares, enemy_pieces & rook2_comp)
        v2 = SlidingPieces.get_vertical_moves(rook2, empty_squares, enemy_pieces & rook2_comp)

        rook1_moves = h1 | v1
        rook2_moves = h2 | v2

        unique_post_move_bitboards = []

        #rook 1
        while(rook1_moves > 0 and rook1 > 0):

            #lsb
            lsb = Bitboard.get_lsb(rook1_moves)

            final_board = lsb | rook2
            unique_post_move_bitboards.append(final_board)

            rook1_moves = Bitboard.remove_lsb(rook1_moves, lsb)

        #rook 2
        while(rook2_moves > 0 and rook2 > 0):

            #lsb
            lsb = Bitboard.get_lsb(rook2_moves)

            final_board = lsb | rook1
            unique_post_move_bitboards.append(final_board)

            rook2_moves = Bitboard.remove_lsb(rook2_moves, lsb)

        return unique_post_move_bitboards
    

    def all_bishop_moves(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff, info_bitboard=None):

        bishop1 = Bitboard.get_lsb(bitboard)
        bishop2 = Bitboard.remove_lsb(bitboard, bishop1)

        bishop1_moves = SlidingPieces.get_diagonal_moves(bishop1, empty_squares, enemy_pieces)
        bishop2_moves = SlidingPieces.get_diagonal_moves(bishop2, empty_squares, enemy_pieces)

        unique_post_move_bitboards = []

        #rook 1
        while(bishop1_moves > 0 and bishop1 > 0):

            #lsb
            lsb = Bitboard.get_lsb(bishop1_moves)

            final_board = lsb | bishop2
            unique_post_move_bitboards.append(final_board)

            bishop1_moves = Bitboard.remove_lsb(bishop1_moves, lsb)

        #rook 2
        while(bishop2_moves > 0 and bishop2 > 0):

            #lsb
            lsb = Bitboard.get_lsb(bishop2_moves)

            final_board = lsb | bishop1
            unique_post_move_bitboards.append(final_board)

            bishop2_moves = Bitboard.remove_lsb(bishop2_moves, lsb)

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
    
    # def get_left_horizontal_ray(bitboard, empty_squares, enemy_pieces, debug_message=None):

    #     #debugging
    #     if not debug_message == None:
    #         print(debug_message)


    #     #get left blocker by right shifting *index* number of times
    #     index = SlidingPieces.get_index(bitboard)
    #     empty_flag = False
    #     empty_num_bits_to_left = int(math.log2(max(Bitboard.get_lsb(Bitboard.complement(empty_squares) >> index), 1)))
    #     enemy_num_bits_to_left = int(math.log2(max(Bitboard.get_lsb(enemy_pieces >> index), 1)))


      
    #     #if closest blocker is less than (and not) an enemy, then the ray needs to be shorter
    #     if empty_num_bits_to_left < enemy_num_bits_to_left:
    #         empty_flag = True

    #         print(empty_num_bits_to_left, "empty1")
    #         print(enemy_num_bits_to_left, "enemy1")
    #     else:
    #         print(empty_num_bits_to_left, "non-empty")
    #         print(enemy_num_bits_to_left, "enemy square")

    #     #if stuck against a friendly piece
    #     if empty_num_bits_to_left == 0 :
    #         print("Abort")
    #         return 0

    #     num_bits_to_left = min(empty_num_bits_to_left, enemy_num_bits_to_left)

 

    #     #find left blocker index (or the wall, if first)
    #     max_left_blocker_index = (index // 8) * 8 + 7

    #     #determine if wall is the limiting reactant here
    #     if max_left_blocker_index < index + num_bits_to_left:
    #         left_blocker_index = max_left_blocker_index
    #         empty_flag = False
    #     else:
    #         left_blocker_index = index + num_bits_to_left

    #     # left_blocker_index = min(index + num_bits_to_left, max_left_blocker_index)

    #     # #empty flag irrelevant if max_left_blocker_index is used
    #     # if left_blocker_index == max_left_blocker_index:
    #     #     empty_flag = False

    #     if num_bits_to_left == 0:
    #         left_blocker_index = max_left_blocker_index

    #     #generate left ray
    #     ray_length = (left_blocker_index - index)
    #     if empty_flag:
    #         ray_length = max(0, ray_length-1)
    #     return  (2 ** (ray_length) - 1) << (index+1)


    def get_left_horizontal_ray(bitboard, empty_squares, enemy_pieces, debug_message=None):

        #find distance to wall
        rook_index = SlidingPieces.get_index(bitboard)
        if rook_index == 99:
            return 0x0
        dist_from_RIGHT_wall = rook_index % 8
        dist_from_LEFT_wall = 7 - dist_from_RIGHT_wall

        #find distance to closest enemy piece AFTER rook_index
        enemy_pieces_shifted = enemy_pieces >> rook_index
        dist_from_enemy = SlidingPieces.get_index(Bitboard.get_lsb(enemy_pieces_shifted))

        #find distance to closest piece (in general) AFTER rook_index
        blockers = Bitboard.complement(empty_squares) & Bitboard.complement(bitboard)
        blockers_shifted = blockers >> rook_index
        dist_from_blocker = SlidingPieces.get_index(Bitboard.get_lsb(blockers_shifted)) - 1

        # Bitboard.print(blockers_shifted, "blockers shifted")

        # print(debug_message)
        # print(dist_from_LEFT_wall, "left wall")
        # print(dist_from_enemy, "enemy")
        # print(dist_from_blocker, "blocker")

        limiting_reactant = int(min(dist_from_LEFT_wall, min(dist_from_enemy, dist_from_blocker)))

        # print("limiting reactant", limiting_reactant)

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
    





    
    # def rotate90_clockwise(bb):
    #     bb = ((bb & 0x0101010101010101) << 7) | \
    #         ((bb & 0x0202020202020202) << 5) | \
    #         ((bb & 0x0404040404040404) << 3) | \
    #         ((bb & 0x0808080808080808) << 1) | \
    #         ((bb & 0x1010101010101010) >> 1) | \
    #         ((bb & 0x2020202020202020) >> 3) | \
    #         ((bb & 0x4040404040404040) >> 5) | \
    #         ((bb & 0x8080808080808080) >> 7)
    #     return bb
    
    # def rotate90_counterclockwise(bb):
    #     bb = ((bb & 0x0101010101010101) << 56) | \
    #         ((bb & 0x0202020202020202) << 40) | \
    #         ((bb & 0x0404040404040404) << 24) | \
    #         ((bb & 0x0808080808080808) << 8)  | \
    #         ((bb & 0x1010101010101010) >> 8)  | \
    #         ((bb & 0x2020202020202020) >> 24) | \
    #         ((bb & 0x4040404040404040) >> 40) | \
    #         ((bb & 0x8080808080808080) >> 56)
    #     return bb



    # #45 degrees to the right
    # def rotate_bitboard(bitboard, empty_squares=0xffffffffffffffff, enemy_pieces=0xffffffffffffffff):

    #     index = SlidingPieces.get_index(bitboard)
    #     s = Bitboard.to_string(enemy_pieces)[::-1]

    #     to_ret = 0x0

    #     #top left
    #     y = index // 8
    #     i = index+9
    #     while(i < 64):
            
    #         if s[i] == "1":
    #             to_ret |= (2 ** (8*y + (i%8)))
    #         i += 9

    #     #top right
    #     x = index % 8
    #     i = index+7
    #     while(i < 64):
            
    #         if s[i] == "1":
    #             to_ret |= (2 ** (i//8 + (x)))
    #         i += 7

    #     return to_ret







        
        
        
        
    #     # final_rotated = 0x0

    #     # for i in range(4):

    #     #     bb = bitboard
    #     #     ep = enemy_pieces

    #     #     for j in range(i):
    #     #         bb = SlidingPieces.rotate90_counterclockwise(bb)
    #     #         ep = SlidingPieces.rotate90_counterclockwise(ep)

    #     #     index = SlidingPieces.get_index(bb)

    #     #     Bitboard.print(bb, "bb")
    #     #     Bitboard.print(ep, "ep")

    #     #     #mask ep
    #     #     ep &= 0xf0f0f0f000000000

    #     #     b = ep >> index
    #     #     b = 0xfffffffffffffffe & b

    #     #     Bitboard.print(b, 'B')
    #     #     print("index", index)

    #     #     counter = 0
    #     #     while b > 0 and b % 2 == 0 and counter < 8:

    #     #         counter += 1
    #     #         b = b >> 9

    #     #     new_b = (2 ** counter - 1) << (index + 1)

    #     #     for j in range(i):
    #     #         new_b = SlidingPieces.rotate90_clockwise(new_b)

    #     #     Bitboard.print(new_b, "new-b")

    #     #     final_rotated |= new_b



    #     # return final_rotated

        








    