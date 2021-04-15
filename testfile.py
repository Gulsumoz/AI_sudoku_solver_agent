


import time
import copy

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.value = '-'
        self.constraints = set()

    def set_constraints(self, constraints):
        self.constraints = constraints

    def set_value(self, value):
        self.value = value

    def __lt__(self, other):
        if len(self.constraints) < len(other.constraints):
            return True



board = []

def main():
    global board
    with open('easy1.txt', 'r') as f:
        data = f.readlines()  # read raw lines into an array

        for i in range(len(data)):
            board.append(data[i].strip('\n'))
        #print(board)
    for idx, line in enumerate(board):

        board[idx] = list(line)
    cells = []
    for n in range(16):
        for m in range(16):
            if board[n][m] == '-':
                cells.append(Cell(n, m))

    # print puzzle in its initial state
    print('puzzle in initial state\n ')
    for c in board:
        print(' '.join(c))

    print("\n")
    solve()
    print("puzzle final state\n")

    printBoard()



def solve():
    global board


    try:
        fillAllObvious()

    except:
        return False

    if isComplete():
        return True

    i, j = 0, 0
    for rowIdx, row in enumerate(board):
        for colIdx, col in enumerate(row):
            if col == "-":
                i, j = rowIdx, colIdx

    possibilities = getPossibilities(i, j)
    for value in possibilities:
        snapshot = copy.deepcopy(board)

        board[i][j] = value

        result = solve()
        if result == True:
            return True
        else:
            board = copy.deepcopy(snapshot)

    return False


def fillAllObvious():
    global board

    while True:
        somethingChanged = False
        for i in range(0, 16):
            for j in range(0, 16):
                possibilities = getPossibilities(i, j)
                if possibilities == False:
                    continue

                if len(possibilities) == 0:
                    raise RuntimeError("No moves left")
                if len(possibilities) == 1:
                    board[i][j] = possibilities[0]
                    somethingChanged = True

        if somethingChanged == False:
            return


def getPossibilities(i, j):
    global board
    if board[i][j] != "-":
        return False

    domain_set = set()
    for line in board:
        for a in line:
            if a != '-':
                domain_set.add(a)
    if len(domain_set) != 16:
        print("File does not contain valid puzzle; there should be 16 unique element")
    # print("domain set\n", domain_set)

    possibilities = domain_set

    for val in board[i]:
        possibilities -= set(val)

    for idx in range(0, 16):
        possibilities -= set(board[idx][j])

    iStart = (i // 4) * 4
    jStart = (j // 4) * 4

    subboard = board[iStart:iStart + 3]
    for idx, row in enumerate(subboard):
        subboard[idx] = row[jStart:jStart + 3]

    for row in subboard:
        for col in row:
            possibilities -= set(col)

    return list(possibilities)


def printBoard():

    global board
    for row in board:
        for col in row:
            print(col, end=" ")
        print(" ")


def isComplete():
    for row in board:
        for col in row:
            if (col == "-"):
                return False

    return True


main()