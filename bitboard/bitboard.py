'''
Basic bitboard class
'''

#useful hex translations
'''

0 = 0000
1 = 0001
2 = 0010
3 = 0011
4 = 0100
5 = 0101
6 = 0110
7 = 0111
8 = 1000
9 = 1001
a = 1010
b = 1011
c = 1100
d = 1101
e = 1110
f = 1111


EXAMPLES:

a row of pawns:   11010011   can be written as d3



'''

class Bitboard:

    def __init__(self, bitboard=0x0000000000000000):
        self.bitboard = bitboard #note that hex is easier to read than binary

    #get complement
    def complement(bitboard):
        return (~bitboard) & 0xffffffffffffffff
    
    
    #converts bitboard into 64 char string
    def to_string(bitboard):
        raw_string = str(bin(bitboard))

        #get rid of the "0b"
        string = raw_string[2:]

        #add leading 0s (if needed)
        to_ret = (64-len(string)) * "0" + string

        return to_ret
    
    #override python print function for clean printing of bitboards
    def print(bitboard, message=""):

        to_ret = ""

        bitstring = Bitboard.to_string(bitboard)

        to_ret += "\nBitboard: " + message + '\n'

        for i in range(8):
            start1 = i*8
            end1 = start1+4

            start2 = start1+4
            end2 = start2+4

            substring = bitstring[start1:end1] + " " + bitstring[start2:end2]

            to_ret += "\n" + substring

        to_ret += '\n'
        
        print(to_ret)
        


    