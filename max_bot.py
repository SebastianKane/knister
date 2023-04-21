from dice_util import *
from math import ceil
from itertools import permutations as perm
from copy import deepcopy

def likely_remaining(num:int):
    '''
    This function takes in a number of empty spaces in a board and returns the 
    most likely set of rolls to occur for the remainder of the game.
    '''
    out = sorted([(x,roll_worlds(x)*num/36) for x in range(2,13)], key = lambda x:x[1]%1, reverse = True)
    diff = num - sum([int(x[1]) for x in out])  
    out = sorted([(x[0],ceil(x[1])) for x in out[0:diff]] + [(x[0],int(x[1])) for x in out[diff:]], key = lambda x:x[0], reverse = True)
    return dict(out)

def best_likely_board(board = [[0]*5 for x in range(5)]):
    best_board = (None, 0)
    queue = [board]
    traveled = set()
    while queue:
        print(best_board[1], len(traveled))
        curr_board = queue.pop()
        #print(curr_board)
        if ' 0' in str(curr_board):
            for i in range(0,12):
                curr_vals = [x for x in get_vals(i, curr_board) if x !=0]
                scores = sorted(all_scores(curr_vals), key = lambda x:x[1], reverse = True)[:10]
                scores = [x[0]+curr_vals+[0]*(5-len(x[0])-len(curr_vals)) for x in scores]
                for score in scores:
                    #TODO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #Seperation of score and current vals needs to be made here. Permutations on complete slice is ineffective
                    for score_perm in set(perm(score)):
                        curr = deepcopy(curr_board)
                        #print(score_perm)i
                        set_vals(i, curr, list(score_perm))
                        if str(curr) not in traveled:
                            traveled.add(str(curr))
                            queue.append(curr)
        else:
            curr_score = score_board(curr_board) 
            if curr_score > best_board[1]:
                best_board = (board, curr_score)
    else:
        return best_board





    


