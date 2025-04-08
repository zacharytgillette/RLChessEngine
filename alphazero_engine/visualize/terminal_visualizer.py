from bitboard.bitboard import *

#very basic engine graphics in termainl, will replace with GUI version later
class TerminalVisualizer:

    def __init__(self):
        pass

    def add_piece_symbols(self, current_string, bitboard, symbol):

        s = Bitboard.to_string(bitboard)
        to_ret = ""

        for i in range(64):
            if s[i] == "1":
                to_ret += symbol
            else:
                to_ret += current_string[i]

        return to_ret

    #simple visualize
    def visualize(self, game, old_index, new_index, capture=None):

        s = "." * 64
        for piece in game.pieces:
            s = self.add_piece_symbols(s, game.pieces[piece].bitboard, game.pieces[piece].symbol)

        print("")
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

            print("")