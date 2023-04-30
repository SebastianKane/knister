from dice_util import *
from math import ceil
from itertools import chain
from itertools import permutations as perm
from copy import deepcopy
from collections import Counter
from bisect import insort

temp = [(Counter(x[0]),x[1]) for x in all_scores([])]
SCORES = []
for x in SCORES:
    if not x in SCORES:
        SCORES.append(x)
SCORES = sorted(SCORES, key = lambda x:x[1], reverse=True)
print(len(SCORES))

def pop_max(queue:list):
    max_item = (0,0,0,-1)
    max_index = 0
    for index, item in enumerate(queue):
        if item[1] > 11:
            del queue[index]
            return item
        if item[3]-(item[1]) > max_item[3]-(max_item[1]):
            max_item = item
            max_index = index
    del queue[max_index]
    #print(max_item)
    return max_item

def likely_remaining(num:int):
    '''
    This function takes in a number of empty spaces in a board and returns the 
    most likely set of rolls to occur for the remainder of the game.
    '''
    out = sorted([(x,roll_worlds(x)*num/36) for x in range(2,13)], key = lambda x:x[1]%1, reverse = True)
    diff = num - sum([int(x[1]) for x in out])  
    out = sorted([(x[0],ceil(x[1])) for x in out[0:diff]] + [(x[0],int(x[1])) for x in out[diff:]], key = lambda x:x[0], reverse = True)
    return Counter(dict(out))
def best_likely_board(board = [[0]*5 for x in range(5)]):
    remaining = likely_remaining(list(chain.from_iterable(board)).count(0))
    best_board = (None, 0)
    queue = [(board,0,0,0)]
    traveled = set()
    high_score = 0

    while queue:
        queue = queue
        #queue = sorted(queue, key = lambda x:x[3], reverse = True)
        #curr_board = queue.pop(0)
        curr_board = pop_max(queue)
        if queue:
            queue_score=score_board(queue[0][0])
            if queue_score > high_score:
                high_score = queue_score
        curr_count = Counter(list(chain.from_iterable(curr_board[0])))
        del curr_count[0]
        print(best_board, len(queue), len(traveled), curr_board)
        #print(curr_board)
        if curr_board[1] < 12:
            for i in range(0,12):
                curr_vals = get_vals((i+curr_board[2])%12, curr_board[0])
                non_z_vals = [x for x in curr_vals if x != 0]
                scores = sorted(all_scores(non_z_vals), key = lambda x:x[1], reverse = True)
                scores = [x for x in scores if Counter(x[0])+curr_count <= remaining][:3]
                if not scores:
                    queue.insert(0, (curr_board[0], curr_board[1]+1, i, curr_board[3]))
                    break
                for score in scores:
                    curr_score=(5-len(score[0])-len(non_z_vals))*[0]+score[0]
                    curr = deepcopy(curr_board[0])
                    #print(score_perm, curr_vals)
                        
                    set_vals((i+curr_board[2])%12, curr, zip_empty(curr_vals.copy(),list(curr_score)))
                    if str(curr) not in traveled:
                        traveled.add(str(curr))
                        curr_board_score = score_board(curr)
                        #if curr_board_score > high_score:
                               # high_score = curr_board_score
                               # best_board = (curr, curr_board_score)
                              #  queue.insert(0, (curr, curr_board[1]+1, (i+1)%12))
                            #else:
                            #insort(queue,(curr, curr_board[1]+1, (i+1)%12), key = lambda x:score_board(x[0]))
                        queue.insert(0, (curr, curr_board[1]+1, (i+1)%12, score_board(curr)))
        else:
            curr_score = score_board(curr_board[0]) 
            if curr_score > best_board[1]:
                best_board = (curr_board[0], curr_score)
    else:
        return best_board

def mult_sets(vals:list) -> set:
    out =[]
    u_vals = set(vals)
    empties = 0
    if not vals:
        for x in range(1,13):
            for y in range(1,6):
                out.append([x]*y)
        for pair in list(combinations(list(range(1,13)),2)):
            out.append([pair[0]]*2+[pair[1]]*2)
            out.append([pair[0]]*2+[pair[1]]*3)
            out.append([pair[0]]*3+[pair[1]]*2) 
    elif 0 in vals:
        empties = vals.count(0)
        vals = [x for x in vals if x != 0]
    else:
        empties = 5 - len(vals)
    for x in range(1,empties+1):
        for val in u_vals:
            out.append([val]*x)
    for pair in list(combinations(u_vals,2)):
        for x in range(1,empties):
            for y in range(1, empties-x+1):
                out.append([pair[0]]*x+[pair[1]]*y)
    return sorted([(x, score_vals(x+vals)) for x in out], key = lambda x:x[1], reverse = True)

class Bstate():
    def __init__(self, board = [[0]*5 for x in range(5)] ):
        self.board = board
    def __str__(self):
        '''
        Takes in a 5x5 2D list representing a knister board and turns it into
        a prettified string for standard output.
        '''
        out=""
        for row in self.board:
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
    def copy(self):
        return Bstate(deep_copy(self.board))
    def get_slice(self, loc:int)->list:
        '''
        This gets the values of groups of elements in a 5x5 2D list using the 
        following key for the loc parameter:
        0: Descending Diag
        1: Ascending Diag
        2-6: Rows 1-5
        7-11: Columns 1-5
        This returns the corresponding slice of the board
        '''
        if loc == 0:
            return [self.board[4-i][i] for i in range(5)]
        elif loc == 1:
            return [self.board[i][i] for i in range(5)]
        elif loc < 7:
            return self.board[loc-2]
        else:
            return list(list(zip(*self.board))[loc-7])
    def slices_to_coords(slice1:int, slice2:int) -> tuple:
        '''
        Takes in two board slice indices and returns a tuple of board coordinates
        where they intersect.
        Example:
        Ascending Diagonal -> Index 0
        Descending Diagonal -> Index 1
        slices_to_coords(0,1) -> (2,2) (Where both diagonals intersec)
        '''
        slices = {slice1, slice2}
        if 0 in slices and 1 in slices:
            return (2,2)
        elif 0 in slices:
            num = ((list(slices-{0})[0]-2) %5) #This works don't be a dummy
            return (4-num, num)
        elif 1 in slices:
            num = ((list(slices-{1})[0]-2) %5) #This works don't be a dummy
            return (num, num)
        else:
            slices = sorted(slices)
            return (slices[0]-2, slices[1]-7)
    def has_zeroes(self):
        for row in self.board:
            if 0 in row:
                return True
    def coords_to_slices(y:int, x:int):
        out = []
        if 4-y == x:
            out.append(0)
        if y == x:
            out.append(1)
        out+=[y+2,x+7]
        return out
    def find_best_state(self):
        out = self.copy()
        while out.has_zeroes():
            for slice1 in range(12):
                for other in range(12):
                    slice2= (slice1+other) % 12




def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3
