import random
import math
from bitboard import *


vertical_values = {
    0: 0,
    1: 1,
    2: 257,
    3: 65793,
    4: 16843009,
    5: 4311810305,
    6: 1103823438081,
    7: 282578800148737
}

horizontal_values = {
    0: 0,
    1: 1,
    2: 3,
    3: 7,
    4: 15,
    5: 31,
    6: 63,
    7: 127
}

def get_north_ray_bitboard(length, x, y, value=None):

    if value == None:
        value = vertical_values[length]
    shift = max(8*(y+1) + (8-x-1), 0)
    value <<= shift
    return value


def get_south_ray_bitboard(length, x, y, value=None):

    if value == None:
        value = vertical_values[length]
    shift = max(8*(y-length) + (8-x-1), 0)
    value <<= shift
    return value


def get_east_ray_bitboard(length, x, y, value=None):

    if value == None:
        value = horizontal_values[length]
    shift = max(8*(y) + (8-x-1) - length, 0)
    value <<= shift
    return value

def get_west_ray_bitboard(length, x, y, value=None):

    if value == None:
        value = horizontal_values[length]
    shift = max(8*(y) + (8-x-1) + 1, 0)
    value <<= shift
    return value



def get_rook_attack_bitboard_dict():

    '''
y
    
7    . . . . . . . . 
6    . . . . . . . .
5    . . . . . . . .
4    . . . . . . . .
3    . . . . . . . .                    n
2    . . . X . . . .                  w   e
1    . . . . . . . .                    s 
0    . . . . . . . .

     0 1 2 3 4 5 6 7   x
    
    '''

    to_ret = []

    for x in range(8):
        for y in range(8):

            #north has 8 - y = 6 options
            #south has y + 1 = 3 options
            #east has 8 - x = 5 options
            #west has x + 1 = 4 options

            d = {}
            index = 1

            #north direction
            for n in range(0, 8-y):
                north_ray = get_north_ray_bitboard(n, x, y)

                #south direction
                for s in range(0, y+1):
                    south_ray = get_south_ray_bitboard(s, x, y)
                    
                    #east direction
                    for e in range(0, 8-x):
                        east_ray = get_east_ray_bitboard(e, x, y)

                        #west direction
                        for w in range(0, x+1):
                            west_ray = get_west_ray_bitboard(w, x, y)

                            combined = north_ray | south_ray | east_ray | west_ray
                            #message = "(" + str(x) + ", " + str(y) + ") for n: " + str(n) + " s: " + str(s) + " e: " + str(e) + " w: " + str(w) 
                            #Bitboard.print(combined, message)

                            d[index] = combined
                            index += 1

            to_ret.append(d)

    return to_ret




def get_num_relevant_bits(square_number):

    if square_number in [0, 7, 56, 63]:
        return 12
    if (square_number + 1) % 8 == 0 or square_number % 8 == 0:
        return 11
    return 10

# b = 0b1000000001000000001000000001000000001000000001000000001000000001
# Bitboard.print(b)


#this is actually for rook class, but i havent made that yet
def mask_relevant_blockers(full_blocker_bitboard, x, y):

    north = 8 - y - 1
    south = y - 1
    east = 8 - x - 1
    west = x - 1

    n = get_north_ray_bitboard(north, x, y)
    s = get_south_ray_bitboard(south, x, y)
    e = get_east_ray_bitboard(east, x, y)
    w = get_west_ray_bitboard(west, x, y)

    blocker_mask = n | s | e | w

    return full_blocker_bitboard & blocker_mask

# Bitboard.print(mask_relevant_blockers(b, 3, 2))


def get_blocker_bitboards(square_number):

    '''
y
    
7    . . . . . . . . 
6    . . . . . . . .
5    . . . . . . . .
4    . . . . . . . .
3    . . . . . . . .                    n
2    . . . X . . . .                  w   e
1    . . . . . . . .                    s 
0    . . . . . . . .

     0 1 2 3 4 5 6 7   x
    
    '''

    y = square_number // 8
    x = square_number % 8

    #for north and south, create mapping of horizontal bitboards to vertical ones
    horizontal_to_vertical = {}
    for z in range((2**6)):

        s = str(bin(z))[2:]
        v = 0

        for i in range(len(s)):

            v += int(s[len(s) - i -1]) * (2 ** (i*8))

        horizontal_to_vertical[z] = v

    blocker_bitboards = {}
    keys = []

    n_length = max((8-y-1-1), 0)
    n_range = 2 ** n_length
    for n_value in range(n_range):
        north_ray = get_north_ray_bitboard(max(n_length, 0), x, y, horizontal_to_vertical[n_value])

        s_length = max((y-1), 0)
        s_range = 2 ** s_length
        for s_value in range(s_range):
            south_ray = get_south_ray_bitboard(max(s_length, 0), x, y, horizontal_to_vertical[s_value])

            e_length = max((8-x-1-1), 0)
            e_range= 2 ** e_length
            for e_value in range(e_range):
                east_ray = get_east_ray_bitboard(max(e_length, 0), x, y, e_value)

                w_length = max((x-1), 0)
                w_range = 2 ** w_length
                for w_value in range(w_range):
                    west_ray = get_west_ray_bitboard(max(w_length, 0), x, y, w_value)

                    blocker_bitboard = north_ray | south_ray | east_ray | west_ray

                    number_of_ones = bin(blocker_bitboard).count('1')
                    # message = "n: " + str(n_length) + " s: " + str(s_length) + " e: " + str(e_length) + " w: " + str(w_length)
                    # message += " nvalue: " + str(n_value) + " svalue: " + str(s_value) + " evalue: " + str(e_value) + " wvalue: " + str(w_value)
                    
                    

                    if number_of_ones not in blocker_bitboards:
                        blocker_bitboards[number_of_ones] = [blocker_bitboard]
                        keys.append(number_of_ones)
                    else:
                        blocker_bitboards[number_of_ones].append(blocker_bitboard)

    #get final result sorted by number of 1s 
    keys = sorted(keys)
    to_ret = []
    
    for key in keys:
        to_ret += blocker_bitboards[key]

    return to_ret



def get_all_blocker_bitboards():

    to_ret = {}
    for i in range(64):
        to_ret[i] = get_blocker_bitboards(i)

    return to_ret

# Bitboard.print(get_all_blocker_bitboards()[0][0])
# Bitboard.print(get_all_blocker_bitboards()[0][1])
# Bitboard.print(get_all_blocker_bitboards()[0][2])
# Bitboard.print(get_all_blocker_bitboards()[0][3])


# a = get_rook_attack_bitboard_dict()[0][1]
# Bitboard.print(a, "hah")


# d = get_all_blocker_bitboards()
# print(len(d))
# print(len(d[0]))
# Bitboard.print(d[1])


def is_correct_attack_bitboard(blocker_bitboard, rook_attack_bitboard, square_number):

    Y = square_number // 8
    X = square_number % 8

    blocker_string = Bitboard.to_string(blocker_bitboard)
    rook_attack_string = Bitboard.to_string(rook_attack_bitboard)

    #rook_attack_string[63-square_number] = 'R'

    rook_attack_string = rook_attack_string[:63-square_number] + 'R' + rook_attack_string[63-square_number + 1:]
    #print(len(rook_attack_string))

    # Bitboard.print(blocker_bitboard, "blocker")
    # Bitboard.print(rook_attack_bitboard, "blocker")

    #find all the primary blockers

    x = X
    y = Y + 1
    up = 7
    while(up == 7 and y < 8):

        sqr_number = y*8 + x
        if blocker_string[63-sqr_number] == '1':
            up = y

        #increase y
        y += 1

    x = X
    y = Y - 1
    down = 0
    while(down == 0 and y >= 0):

        sqr_number = y*8 + x
        if blocker_string[63-sqr_number] == '1':
            down = y

        #dec y
        y -= 1

    x = X + 1
    y = Y
    right = 7
    while(right == 7 and x < 8):

        sqr_number = y*8 + x
        if blocker_string[63-sqr_number] == '1':
            right = x

        #increase x
        x += 1

    
    x = X - 1
    y = Y
    left = 0
    while(left == 0 and x >= 0):

        sqr_number = y*8 + x
        if blocker_string[63-sqr_number] == '1':
            left = x

        #dec x
        x -= 1

    #(up, down, left, right)

    left_barrier = Y*8 + (left)
    right_barrier = Y*8 + (right)
    up_barrier = (up)*8 + X
    down_barrier = (down)*8 + X

    return (rook_attack_string[63-left_barrier] in ['1', 'R']) and (rook_attack_string[63-right_barrier] in ['1', 'R']) and (rook_attack_string[63-up_barrier] in ['1', 'R']) and (rook_attack_string[63-down_barrier] in ['1', 'R'])

# blocker = 0b0000000000010000000000000000000001000100000000000001000000000000

# attack =  0b0000000000010000000100000001000001101100000100000001000000000000

# print(bin(blocker & attack).count('1') >= 4)

# print(is_correct_attack_bitboard(blocker, attack, 28))



import random

def get_magic_number(square_number):
    blocker_bitboards = get_all_blocker_bitboards()[square_number]
    rook_attack_bitboards = get_rook_attack_bitboard_dict()[square_number]
    num_relevant_bits = get_num_relevant_bits(square_number)

    indices = []

    while len(indices) < 2**num_relevant_bits:
        magic_number = random.randint(2**50, 2**64 - 1)

        for blocker_bitboard in blocker_bitboards:

            
            
            dynamic_shift = 0
            if blocker_bitboard > 0:
            
                dynamic_shift = max(int(math.log2(blocker_bitboard * magic_number)) - 64 + 1, 0)

            index = ((blocker_bitboard * magic_number) >> dynamic_shift) >> (64-num_relevant_bits)

            #print(index)

            if index in indices:
                if len(indices) > 1:
                    print(f"duplicates: {len(indices)}")

                    Bitboard.print(blocker_bitboard)
                    print("failing index", index)
                    print(indices)

                indices = []  # reset indices
                break  # exit the for loop to try another magic number
            else:
                indices.append(index)

    # If we reached here, we found a magic number
    print("BANG")
    print("Magic Number:", magic_number)
    print("Indices:", indices)

# Sample call to the function
get_magic_number(0)


    







def get_magic_numbers():

    blocker_bitboards = get_all_blocker_bitboards()

    rook_attack_bitboards = get_rook_attack_bitboard_dict()

    magic_numbers = {}

    #for each square
    for i in range(1):


        num_relevant_bits = int(math.log2(len(blocker_bitboards[i])))
        #num_relevant_bits = get_num_relevant_bits(i)
        print("relevant bits", num_relevant_bits)

        valid = False
        magic_number = -1
        counter = 0
        while(not valid):
        
            #keep trying magic numbers until we find one that works for
            # ALL blocker bitboards on that square
            magic_number = random.randint(0, 2**64)
            counter += 1
            broke = False

            indices_found = []

            if counter % 1000000 == 0:
                print(counter)


            high_score = 0
            #loop through all blocker bitboards...
            #print(blocker_bitboards)

            #print(blocker_bitboards[i])


            for it in range(len(blocker_bitboards[i])):

                blocker_bitboard = blocker_bitboards[i][len(blocker_bitboards[i])-1-it]

                dynamic_shift = int(math.log2(blocker_bitboard * magic_number)) - 64

                index = ((blocker_bitboard * magic_number) >> dynamic_shift) >> (64-num_relevant_bits)
                index -= 4096
                #print(blocker_bitboard * magic_number)
                #print(index)

                if not index in indices_found:
                    # print("dy", dynamic_shift)
                    # print(magic_number * blocker_bitboard)
                    indices_found.append(index)
                    # print("")
                    # print("found: ", index, len(indices_found))

                if len(indices_found) > 0:

                    print(sorted(indices_found))
                    
                

                #print(blocker_bitboard, "bb")
                rook_attack_bitboard = rook_attack_bitboards[i][index]

                if counter % 1000000 == 0:
                    # Bitboard.print(blocker_bitboard, "blocker bitboard (1)")
                    # Bitboard.print(rook_attack_bitboard, "rook attack bitboard (2)")
                    ...

                #now check if the attack bitboard that the magic number indexes to is the correct one for the blocker

                #first check if the attack shape fits
                if bin(blocker_bitboard & rook_attack_bitboard).count('1') == 4:

                    #now make sure it is actually the correct fitting (no empty space)
                    if is_correct_attack_bitboard(blocker_bitboard, rook_attack_bitboard, i):
                        high_score += 1
                    else:

                        # Bitboard.print(blocker_bitboard, "blocker")
                        # Bitboard.print(rook_attack_bitboard, "rook attack")
                        broke = True
                        break
                        

                else:    
                    broke = True
                    break
                    

                if high_score >= 1:
                    print("woah", high_score)

            if not broke:
                valid = True

        #if valid is still true here, then it is a magic number!
        magic_numbers[i] = magic_number
        print("woo hoo! magic number: ", magic_number)
        print("counter", counter)

    return magic_numbers


# nums = get_magic_numbers()
# print(nums[0])
                    
#    15719170825873196456

# blocker_bitboards = get_all_blocker_bitboards()[0]
# rook_attack_bitboards = get_rook_attack_bitboard_dict()[0]
# num_relevant_bits = int(math.log2(len(blocker_bitboards)))

# print(num_relevant_bits)

# for i in range(3):

#     r = random.randint(0, len(blocker_bitboards)-1)

#     blocker = blocker_bitboards[r]

#     index = (15719170825873196456 * blocker) >> (64 - num_relevant_bits)
#     rook_attack = rook_attack_bitboards[index]

#     Bitboard.print(blocker, "blocker")
    #Bitboard.print(rook_attack, "rook attack")








# for b in s:
#     Bitboard.print(b)
# print(len(s))



#index = (magic_number * blockers) >> (64 - significant_bits)




#d = get_rook_attack_bitboard_dict()


# for i in range(len(d)):

#     print(i, ": ", len(d[i]))




# print(len(d.keys()))

# import random
# r = len(d.keys())
# for i in range(5):

#     ind = random.randint(0, r-1)

#     Bitboard.print(d[list(d.keys())[ind]])

    

