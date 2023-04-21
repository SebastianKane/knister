from dice_util import *
from math import ceil
from itertools import permutations as perm

def likely_remaining(num:int):
    '''
    This function takes in a number of empty spaces in a board and returns the 
    most likely set of rolls to occur for the remainder of the game.
    '''
    out = sorted([(x,roll_worlds(x)*num/36) for x in range(2,13)], key = lambda x:x[1]%1, reverse = True)
    diff = num - sum([int(x[1]) for x in out])  
    out = sorted([(x[0],ceil(x[1])) for x in out[0:diff]] + [(x[0],int(x[1])) for x in out[diff:]], key = lambda x:x[0], reverse = True)
    return dict(out)

def best_likely_board(board = [[0]*5]*5):
    best_scores = sorted(all_scores([7]),key = lambda x:x[1], reverse = True)


