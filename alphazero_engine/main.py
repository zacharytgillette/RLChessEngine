from testing import Test
from bitboard.bitboard import *
import time


def main():


    tester = Test()

    # tester.test_gpt_flipper()

    # return

    #print("Running test_model...")
    #tester.test_model()

    # Uncomment if you want to run training (this may take a while)
    print("Running test_selfplay...")
    tester.test_selfplay()

    #print("Running test_play_model...")
    #tester.test_play_model()

    # start = time.time()
    # for i in range(1000):
    #     print(tester.test_play_model_mass_simulation())
    # print("RUNTIME:", time.time() - start)

if __name__ == "__main__":
    main()





# ** Zach's main testing **

from game import *
# def main():
#
#
#     # rook = Rooks(WHITE, 0x0000000000000004)
#
#     # #case 1: wall blocker
#     # wall_empty = 0xffffffffffffffff
#     # wall_enemy = 0x0000000000000000
#
#     # #case 2a: enemy blocker (edge)
#     # enemy_blocker_edge_empty = 0xffffffffffffff7f
#     # enemy_blocker_edge_enemy = 0x0000000000000080
#
#     # #case 2b: enemy blocker (not-edge)
#     # enemy_blocker_non_edge_empty = 0xffffffffffffffdf
#     # enemy_blocker_non_edge_enemy = 0x0000000000000020
#
#     # #case 3a: friendly blocker (edge)
#     # friendly_blocker_edge_empty = 0xffffffffffffff7f
#     # friendly_blocker_edge_enemy = 0x0000000000000000
#
#     # #case 3b: friendly blocker (not edge)
#     # friendly_blocker_non_edge_empty = 0xffffffffffffffff
#     # friendly_blocker_non_edge_enemy = 0x0000000000000000
#
#     # #tests
#     # SlidingPieces.get_left_horizontal_ray(rook.bitboard, friendly_blocker_non_edge_empty, friendly_blocker_non_edge_enemy)
#     # Bitboard.print(friendly_blocker_non_edge_empty, "empty squares")
#     # Bitboard.print(friendly_blocker_non_edge_enemy, "ENEMY squares")
#     # Bitboard.print(SlidingPieces.get_left_horizontal_ray(rook.bitboard, wall_empty, wall_enemy), "ANSWER")
#
#
#
#
#
#     for i in range(1000000):
#
#         game = Game()
#         res = game.simulate_game()
#
#         if res == 1 or res == 2:
#             quit()
#
#
#
#
#
#
#     # queen = Queens(WHITE, 0x0000000400000000)
#     # rook = Rooks(WHITE, 0x0000000000000080)
#     # bishop = Bishops(WHITE, 0x0000000400000000)
#
#     # blocker = 0b1111111111110111000000000000100000010000000000001110111111111111
#     # empty = Bitboard.complement(blocker)
#
#     # blocker = 0b1000000000000000000000000000000000000000000000000000000000000001
#     # empty = 0b0111111111111111111111111111111111111111111111111111111111111110
#
#     # open_squares = 0x00ffffffffffff00
#     # enemy_squares = 0xff00000000000000
#
#     # empty_squares = 0b0000000000001000111101111111111101111111111111111000000000000000
#     # enemy_pieces = 0b1111111111110111000010000000000000000000000000000000000000000000
#
#     # Bitboard.print(rook.bitboard, "rook")
#     # Bitboard.print(empty_squares, "open squares")
#     # Bitboard.print(enemy_pieces, "enemy squares")
#
#     # moves = rook.all_moves(empty_squares, enemy_pieces)
#
#     # all_moves = 0x0
#
#     # for move in moves:
#
#     #     # Bitboard.print(move, "move")
#
#     #     all_moves |= move
#
#     # Bitboard.print(all_moves, "all moves")
#
#
#
#
#
# if __name__ == "__main__":
#     main()
