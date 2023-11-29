import math
import random
from sympy import isprime


###################### OT -> Integer

def text_to_vector(OT):
    vector = []
    while len(OT) >= 5:
        vector.append(block_to_int(OT[-5:]))
        # print(OT[-5:], " \tnum: ", vector)
        OT = OT[0:-5]

    if len(OT) > 0:
        vector.append(block_to_int(OT))
        # print(OT, "  \tnum: ", vector)

    return vector[::-1]


def block_to_int(blk):
    bin_string = ""

    for c in blk:
        bin_string += int_to_bin(ord(c))

    return int(bin_string, 2)


# 8-bit codification of a given integer
def int_to_bin(n):
    bin_string = bin(n)[2:]
    return (8 - len(bin_string)) * '0' + bin_string


###################### Integer -> OT

def vector_to_text(vector):
    OT = ""
    for n in vector:
        OT += int_to_block(n)

    return OT


def int_to_block(num):
    blk = ""
    bin_string = bin(num)[2:]
    bin_string = (8 - (len(bin_string) % 8)) * '0' + bin_string

    for i in range(0, len(bin_string), 8):
        blk += chr(int(bin_string[i:i + 8], 2))
        # print(i, "\t", bin_string[i:i+8])

    return blk


###################### Encryption and decryption

def encryption(OT, e, n):
    return pow(OT, e, n)


def decryption(CT, d, n):
    return pow(CT, d, n)


if __name__ == '__main__':
    vector = text_to_vector("This is a plain-text")

    print(vector_to_text(vector))

# 112 key
