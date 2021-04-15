# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 15:56:16 2019

@author: gulsum
"""
import time
import copy

board = [
    "JNIH----EGFDAMCO",
    "--BOM-F-P-L--IH-",
    "-K--A--H-BCIF-LN",
    "-GCF-EJ-ANM---DP",
    "AJ--OGHFNCIEB--D",
    "-EG-PKA--M--HFNC",
    "-DM--J-EG--FPL-A",
    "CF-KN-I-BAD-EO-G",
    "KPAC-NOB-D-MJ-F-",
    "FO-IE-CMH-B--DGK",
    "M-NL-P-JIK-COAE-",
    "---DHIK-FO-JM---",
    "PI--JA--K-H-L-B-",
    "-COEB-N--L-GD-KJ",
    "--FJDOMK--PN-G--",
    "N-KA--PG-IJBCE-F"
]

assignment = 0


def main():
    global board
    global assignment
    for idx, line in enumerate(board):
        # print(enumerate(board))
        board[idx] = list(line)
    # print(board)
    starting_time = time.time()

    solve()
    end_time = time.time()
    total_time = end_time - starting_time
    print(total_time)
    print(assignment)
    printBoard()


def solve():
    global board
    global assignment

    try:
        fillAllObvious()
        assignment += 1
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

    return False, assignment


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
            print(col, end="")
        print("")


def isComplete():
    for row in board:
        for col in row:
            if (col == "-"):
                return False

    return True


main()