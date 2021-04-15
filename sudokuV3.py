#!/usr/bin/env python

import sys
import os.path
import time


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.square = get_square_membership(row, col)
        self.value = '-'
        self.constraints = set()

    def set_constraints(self, constraints):
        self.constraints = constraints

    def set_value(self, value):
        self.value = value

    def __lt__(self, other):
        if len(self.constraints) < len(other.constraints):
            return True


cell_assignments = 0


def update_assignments():
    global cell_assignments
    cell_assignments += 1


def print_assignments():
    return cell_assignments


def main(pzfile):

    puzzle_file = open(pzfile, 'r')
    lines = [line.rstrip() for line in puzzle_file]
    puzzle_file.close()

    # validate puzzle format
    if len(lines) != 16:
        sys.exit('File does not contain valid puzzle, there should be 16 row')
    for i, line in enumerate(lines):
        if len(line) != 16:
            sys.exit('File does not contain valid puzzle, there should be 16 column')

    # we can create the domain set of 16 unique symbol used in 16x16 sudoku

    domain_set = set()
    for line in lines:
        for a in line:
            if a != '-':
                domain_set.add(a)
    if len(domain_set) != 16:
        sys.exit("File does not contain valid puzzle; there should be 16 unique element")

    # we can create sudoku matrix
    sudoku_matrix = []
    for line in lines:
        row = []
        for t in line:
            row.append(t)
        sudoku_matrix.append(row)
    # this matrix is representation og 16X16 sudoku puzzle
    sudoku_puzzle = sudoku_matrix

    # we can create row set and test if row has any duplicate values
    rows = []
    for y in sudoku_puzzle:
        row = set()
        for z in y:
            if z != '-':
                if z in row:
                    sys.exit('there are duplicate values in the row puzzle is not valid')
                else:
                    row.add(z)
        rows.append(row)

    # create column set and test if there is a duplicate item
    cols = []
    for n in range(16):
        col = set()
        for m in range(16):
            if sudoku_puzzle[m][n] != '-':
                if sudoku_puzzle[m][n] in col:
                    sys.exit('there are duplicate values in the colum of the puzzle')
                else:
                    col.add(sudoku_puzzle[m][n])
        cols.append(col)

    # create 4x4 square sets
    squares = []
    for n in range(16):
        squares.append(set())
    for a in range(16):
        for b in range(16):
            if sudoku_puzzle[a][b] != '-':
                square = get_square_membership(a, b)
                if sudoku_puzzle[a][b] in squares[square]:
                    sys.exit("there are duplicate values in the square")
                else:
                    squares[square].add(sudoku_puzzle[a][b])

    # creating sudoku cells variables
    cells = []
    for n in range(16):
        for m in range(16):
            if sudoku_puzzle[n][m] == '-':
                cells.append(Cell(n, m))

    # print puzzle in its initial state
    print('puzzle in initial state ')
    for c in sudoku_puzzle:
        print(' '.join(c))

    # this is for tracking the time
    starting_time = time.time()



    if csp_mrv(cells, rows, cols, squares, domain_set):
        print('Solution found!')
        end_time = time.time()
        total_time = end_time - starting_time
        total_num_assignment = print_assignments()
        print('Number of assignments: ' + str(total_num_assignment))
        print('Total time to solve the puzzle: ' + str(total_time) + ' seconds')
        finished_puzzle = sudoku_puzzle
        for cl in cells:
            finished_puzzle[cl.row][cl.col] = cl.value
        for a in finished_puzzle:
            print(' '.join(a))
    else:
        print('No solution found!')






def csp_mrv(cells, rows, cols, squares, domain_set):
    if constraint_sort(cells, rows, cols, squares, domain_set):
        cell = cells.pop(0)
        for constraint in cell.constraints:
            cell.set_value(constraint)
            update_assignments()
            rows[cell.row].add(cell.value)
            cols[cell.col].add(cell.value)
            squares[cell.square].add(cell.value)

            if goal(rows, cols, squares):
                cells.insert(0, cell)
                return True
            else:
                if cells:
                    if csp_mrv(cells, rows, cols, squares, domain_set):
                        cells.insert(0, cell)
                        return True
                    else:
                        rows[cell.row].discard(cell.value)
                        cols[cell.col].discard(cell.value)
                        squares[cell.square].discard(cell.value)
                        cell.set_value('-')
                else:
                    rows[cell.row].discard(cell.value)
                    cols[cell.col].discard(cell.value)
                    squares[cell.square].discard(cell.value)
                    cell.set_value('-')

        cells.insert(0, cell)
        return False
    else:
        return False


def constraint_sort(cells, rows, cols, squares, domain_set):
    for cell in cells:
        constraints = domain_set - (rows[cell.row] | cols[cell.col] | squares[cell.square])
        if constraints:
            cell.set_constraints(constraints)
        else:
            return False
    cells.sort()
    return True


def get_square_membership(row, col):
    if 0 <= row <= 3:
        if 0 <= col <= 3:
            return 0
        elif 4 <= col <= 7:
            return 1
        elif 8 <= col <= 11:
            return 2
        elif 12 <= col <= 15:
            return 3
    elif 4 <= row <= 7:
        if 0 <= col <= 3:
            return 4
        elif 4 <= col <= 7:
            return 5
        elif 8 <= col <= 11:
            return 6
        elif 12 <= col <= 15:
            return 7
    elif 8 <= row <= 11:
        if 0 <= col <= 3:
            return 8
        elif 4 <= col <= 7:
            return 9
        elif 8 <= col <= 11:
            return 10
        elif 12 <= col <= 15:
            return 11
    elif 12 <= row <= 15:
        if 0 <= col <= 3:
            return 12
        elif 4 <= col <= 7:
            return 13
        elif 8 <= col <= 11:
            return 14
        elif 12 <= col <= 15:
            return 15


def goal(rows, cols, squares):
    for row in rows:
        if len(row) != 16:
            return False
    for col in cols:
        if len(col) != 16:
            return False
    for square in squares:
        if len(square) != 16:
            return False
    return True


if __name__ == "__main__":
    main("SudokuPuzzle7.txt")

