"""
=============================================================================
Title    : Matthew_Cabrera_MultiProcessing.py
Description : This is a python program that performs the first 100 iterations 
                of a modified cellular automaton simulator using multiprocessing
Author   : matthcab
Date     : 04/29/2025
Version  : 2.0
=============================================================================
"""

import argparse
import sys
from multiprocessing import Pool

print("Project :: MultiProcessing")

# Mapping symbols to values
symbolValues = {
    'O': 3,   # Healthy O
    'o': 1,   # Weakened O
    '.': 0,   # Dead
    'x': -1,  # Weakened X
    'X': -3   # Healthy X
}
validSymbols = set(symbolValues.keys())


# Numeric sequence functions

# Returns a set containing all Fibonacci numbers up to n_max
def fibonacci(n_max=1000):
    fib = {0, 1}
    a, b = 0, 1
    while b <= n_max:
        a, b = b, a + b
        fib.add(a)
    return fib

# Returns True if n is a power of two
def poweroftwo(n):
    return n > 0 and (n & (n - 1)) == 0

# Returns True if n is a prime number
def prime(n):
    if n < 2:
        return False
    for i in range(2, int(abs(n) ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


# Argument parsing

# Parses arguments for input/output files and number of processes
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True)  # input file
    parser.add_argument("-o", required=True)  # output file
    parser.add_argument("-p", type=int, default=1) # multiprocessing
    return parser.parse_args()


# File I/O functions

# Reads a matrix from a file
def readMatrix(file):
    with open(file, 'r') as f:
        matrix = [list(line.strip()) for line in f if line.strip()]
    # Validate rectangular
    if len(set(len(row) for row in matrix)) != 1:
        sys.exit(1)
    # Validate symbols
    for row in matrix:
        for ch in row:
            if ch not in validSymbols:
                sys.exit(1)
    
    return matrix

# Writes a matrix to a file
def writeMatrix(matrix, file):
    with open(file, 'w') as f:
        for i, row in enumerate(matrix):
            f.write(''.join(row))
            if i != len(matrix) - 1:
                f.write('\n')


# Matrix processing helper function

# Processes a chunk of rows in the matrix
def processChunk(startRow, endRow, matrix, fibset, rows, cols):
    newChunk = []

    for r in range(startRow, endRow):
        newRow = []
        for c in range(cols):
            curr = matrix[r][c]
            symbol = 0
            # Compute sum of neighbor values
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = (r + dr) % rows, (c + dc) % cols
                    symbol += symbolValues.get(matrix[nr][nc], 0)
            # Apply transformation rules
            if curr == 'O':
                if symbol in fibset:
                    newRow.append('.')
                elif symbol < 12:
                    newRow.append('o')
                else:
                    newRow.append('O')
            elif curr == 'o':
                if symbol < 0:
                    newRow.append('.')
                elif symbol > 6:
                    newRow.append('O')
                else:
                    newRow.append('o')
            elif curr == '.':
                if poweroftwo(symbol):
                    newRow.append('o')
                elif poweroftwo(abs(symbol)):
                    newRow.append('x')
                else:
                    newRow.append('.')
            elif curr == 'x':
                if symbol >= 1:
                    newRow.append('.')
                elif symbol < -6:
                    newRow.append('X')
                else:
                    newRow.append('x')
            elif curr == 'X':
                if prime(abs(symbol)):
                    newRow.append('.')
                elif symbol > -12:
                    newRow.append('x')
                else:
                    newRow.append('X')

        newChunk.append(newRow)

    return newChunk


# Matrix processing logic

# Applies cellular automaton rules for 100 steps using multiprocessing
def matrixProcessing(matrix, fibset, numProcesses):
    rows = len(matrix)
    cols = len(matrix[0])
    chunkSize = (rows + numProcesses - 1) // numProcesses
    # Create a single Pool and reuse it for all iterations
    with Pool(processes=numProcesses) as pool:
        for i in range(100):
            args = []
            # Split matrix into chunks based on number of processes
            for j in range(numProcesses):
                startRow = j * chunkSize
                endRow = min((j + 1) * chunkSize, rows)
                if startRow < endRow:
                    args.append((startRow, endRow, matrix, fibset, rows, cols))
            # Run processChunk on all chunks in parallel
            resultChunks = pool.starmap(processChunk, args)
            # Puts resultChunks into a single new matrix
            newMatrix = []
            for chunk in resultChunks:
                for row in chunk:
                    newMatrix.append(row)
            matrix = newMatrix  # Updates matrix for next iteration

    return matrix


# Main function
def main():
    try:
        args = parse_args()
        matrix = readMatrix(args.i)
        fibset = fibonacci(8 * len(matrix) * len(matrix[0]) * 3)
        matrix = matrixProcessing(matrix, fibset, args.p)
        writeMatrix(matrix, args.o)
        print("Matrix Processed.")
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
