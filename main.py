import math
import random

def text_to_number(OT):
    return OT

def block_to_int(blk):
    bin_string = ""

    for c in blk:
        bin_string += int_to_bin(ord(c))

    return int(bin_string, 2)


# 8-bit codification of a given integer
def int_to_bin(n):
    bin_string = bin(n)[2:]
    return (8 - len(bin_string)) * '0' + bin_string


if __name__ == '__main__':
    print(block_to_int("AA"))

