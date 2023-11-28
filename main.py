import math
import random

###################### OT -> Integer

def text_to_number(OT):
    num = ""
    while len(OT) >= 5:
        num = str(block_to_int(OT[-5:])) + num
        #print(OT[-5:], " \tnum: ", num)
        OT = OT[0:-5]

    if len(OT) > 0:
        num = str(block_to_int(OT)) + num
        #print(OT, "  \tnum: ", num)

    return num

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

def number_to_text(num):
    bin_ = #112 key

if __name__ == '__main__':
    print(text_to_number("I WANNA TAKE YOU AWAY"))
