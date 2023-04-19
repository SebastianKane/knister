from itertools import combinations
from itertools import combinations_with_replacement as comb
from collections import Counter
from copy import deepcopy
from math import prod
from random import randint
#AVG_POINTS = sum([avg_tot([x]) for x in range(2,13) ])/12
#This is the average between the avg_points of each single value 
#(avg_tot([2,0,0,0,0])+avg_tot([3,0,0,0,0])+...)/12

AVG_POINTS = 0.2697659266562516
def main():
   pass 
def all_straights(vals:list) -> list:
    '''
    Takes in a list of 5 or less values and returns a list of tuples with all 
    the possible straights that can be made using the passed values and their 
    corresponding scores.
    '''
    if score_mults(vals) > 0:
        return []
    out = []
    max_val = max(vals)
    min_val = min(vals)
    if max_val - min_val < 5:
        start = max_val - 4
        end = min_val + 1
        if start < 2:
            start = 2
        if end > 9:
            end = 9
        for val in range(start,end):
            if(val <= 7 and (val + 5) > 7):
                out.append((list(set(range(val, val+5))-set(vals)), 8) )
            else:
                out.append((list(set(range(val, val+5))-set(vals)), 12) )
        return out
    else:
        return out

def get_mults(vals:list) -> list:
    '''
    Takes in a list of 5 or less values and returns a list of all the possible 
    pairs (2 or more) and fullhouses that can be made including the passed in
    values.
    '''
    out = []
    space = 5 - len(vals)
    if 5 - len(vals) > 1:
        if len(set(vals)) > 1:
            if 5 - len(vals) > 1:
                for u_val in (set(range(2,13))-set(vals)):
                    for z in range(2, 6- len(vals)):
                        curr = vals.copy()
                        curr+=[u_val]*z
                        out.append(curr)
            for pair in list(combinations(set(vals),2)):
                for x in range(space+1):
                    for y in range(space-x+1):
                        curr = vals.copy()
                        curr += [pair[0]]*x
                        curr += [pair[1]]*y
                        if x!= 0 or y!=0:
                            out.append(curr)
                            if 5 - len(curr) > 1:
                                 for u_val in (set(range(2,13))-set(curr)):
                                    for z in range(2, 6- len(curr)):
                                        curr2 = curr.copy()
                                        curr2+=[u_val]*z
                                        out.append(curr2)

        else:
            for x in range(1,space):
                curr = vals.copy()
                curr+=[vals[0]]*x
                out.append(curr)
            for u_val in (set(range(2,13))-set(vals)):
                for x in range(2, 6- len(vals)):
                    curr = vals.copy()
                    curr+=[u_val]*x
                    out.append(curr)
            if len(vals) == 1:
                for pair in list(combinations(set(range(2,13))-set(vals),2)):
                    curr = vals.copy()
                    curr += [pair[0]]*2
                    curr += [pair[1]]*2
                    out.append(curr)
    else:
        for u_val in set(vals):
            curr = vals.copy()
            curr+=[u_val]
            out.append(curr)

    return out
                            
                               

            
            

def all_mults(vals:list) -> list:
    '''
    Takes in a list of 5 or less values and returns a list of tuples with all 
    the possible pairs (2 or more) and full houses that can be made using the 
    passed values and their corresponding scores.
    '''

    mults = get_mults(vals)
    out = []
    for mult in mults:
        u_vals = set(mult)
        occurs = [mult.count(x) for x in u_vals]
        if 3 in occurs and 2 in occurs:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 8))
        elif occurs.count(2) == 2:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 2))
        elif 2 in occurs:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 1))
        elif 3 in occurs:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 3))
        elif 4 in occurs:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 6))
        elif 5 in occurs:
            out.append((list((Counter(mult)-Counter(vals)).elements()), 10))
    return out

def score_board(board: list) -> int:
    '''
    Takes in a 5x5 2D list representing a knister board and reeturns a score.
    '''
    out = 0
    #print(board_str(board))
    for row in board:
        out += avg_tot(row)
    for col in list(zip(*board)):
        #print("col:",col)
        out += avg_tot(col)
    diag_1 = [board[i][i] for i in range(len(board))]
    #print(diag_1, avg_tot(diag_1))
    out += avg_tot(diag_1)*2
    diag_2 = [board[i][len(board)-1-i] for i in range(len(board))]
    #print(diag_2)
    out += avg_tot(diag_2)*2
    return out

def make_move(num: int, board =[[0]*5 for i in range(5)] ):
    '''
    Takes in a number representing a roll and a 5x5 2D list representing a 
    knister board state and a 5x5 2D list representing the same board
    state with the adition of one new move.
    '''
    best_board = deepcopy(board)
    best_score = -1
    curr_board = deepcopy(board)
    any_zeros = False
    for row_i, row in enumerate(board):
        for col_i, item in enumerate(row):
            if item == 0:
                any_zeros = True
                curr_board[row_i][col_i] = num
                score = score_board(curr_board)
                #print(score, curr_board)
                if score > best_score:
                    best_score = score
                    best_board = deepcopy(curr_board)
                curr_board = deepcopy(board)
    if not any_zeros:
        print("Score is:",score_board(board))
    #print(best_board)
    return best_board

def avg_tot(vals:list):        
    vals = [i for i in vals if i!=0]
    poss_worlds = pow(36, 5-len(vals))
    #print(poss_worlds, len(vals))
    if not vals:
        return AVG_POINTS
    if len(vals) == 5:
        return score_vals(vals)

    score_opps = all_straights(vals)+all_mults(vals)
    #print(score_opps)
    score_worlds = 0
    score_tot = 0
    
    for opp in score_opps:
        empties = 5-(len(vals)+len(opp[0]))
        slice_worlds = pow(36,empties) * prod([(6 - abs(7-x)) for x in opp[0]])
        #print(opp[0],opp[1],slice_worlds, poss_worlds)
        score_tot+=opp[1]*slice_worlds
        score_worlds+= slice_worlds
    #Every world you don't make points is treated as the number of points vals currently makes
    #score_tot += (poss_worlds - score_worlds) * score_vals(vals)
    score_tot+=(poss_worlds-score_worlds)*score_vals(vals)
    #print(score_tot, score_worlds, poss_worlds)
    #The average is all possible points divided by all possible worlds
    return score_tot/ poss_worlds
      
def is_straight(vals:list) -> bool:
    '''
    Takes in a 5 element list representing a row, column or diagonal and 
    returns if the list is a straight.
    '''
    if len(vals) < 5:
        return 0
    curr = vals[0]
    for item in vals[1:]:
        curr+=1
        if curr!= item:
            return False
    return True
def score_straight(vals:list):
    if is_straight(vals):
        if 7 in vals:
            return 8
        else:
            return 12
    else:
        return 0
def score_vals(vals:list):
     '''
    Takes in a 5 element list representing a row, column or diagonal and 
    returns its score.
    '''
    return score_straight(vals)+score_mults(vals)
def score_mults(vals:list):
    '''
    Takes in a 5 element list representing a row, column or diagonal and 
    returns only the scores of pairs (2 or more) and full houses.
    '''

    if is_straight(vals):
        return 0
    out = []
    curr = 0
    streak = 1
    for item in set(vals):
        out.append(vals.count(item))
    if 3 in out and 2 in out:
        return 8
    elif out.count(2) == 2:
        return 3
    elif 2 in out:
        return 1
    elif 3 in out:
        return 3
    elif 4 in out:
        return 6
    elif 5 in out:
        return 10
    return 0

def roll():
    '''
    Returns a number between 2-12 with a similar probability to 2D6.
    '''
    return randint(2,6)+randint(2,6)

def auto_play() -> int:
    '''
    Starts with an empty knister board and makes_moves until it's full 
    returning the score of the final board. 
    '''
    r = roll()
    out = make_move(r)
    old_out = ""
    r = roll()
    while not str(out) == old_out:
        #print(out, r, score_board(out))
        old_out = str(out)
        out = make_move(r, out)
        print(board_str(out))
        r =roll()
    return out
def board_str(board):
    '''
    Takes in a 5x5 2D list representing a knister board and turns it into
    a prettified string for standard output.
    '''
    out=""
    for row in board:
        out_row = ""
        for item in row:
            item = str(item)
            if len(item) == 1:
                item += " |"
            else:
                item += "|"
            out_row+=item
        out+=out_row[:-1]+"\n"
        out+="-- "*5+"\n"
    return out[:-16]+"\n"

def avg_play(num:int):
    '''
    Auto plays knister a num number of times and returns the average score.
    '''
    tot = sum(score_board(auto_play()) for x in range(num))
    return tot/num
def get_all(vals:list):
    '''
    Returns all possible additionally scoreable states from a 5 element 
    list (vals)with their corresponding scores. This excludes all states with 
    the same score as the initial state.
    '''
    return all_mults(vals)+all_straights(vals)
if __name__ == "__main__":
    main()
