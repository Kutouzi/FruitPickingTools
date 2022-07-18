import random as rd
from itertools import product

def checkErrorCode(errorCode:int):
    if errorCode == 0:
        print("get cg finish.")
        return 0
    elif errorCode == 1:
        print("error network.cant get cg.")
    elif errorCode == 2:
        print("error resource.resource is null in server.")
    elif errorCode == 3:
        print("error output.cant output image or movie.")

def yield_str(chr_start=65,chr_end=90):
    for chs in product(map(chr, range(chr_start, chr_end+1)),repeat=4):
        yield ''.join(chs)