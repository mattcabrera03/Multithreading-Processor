# MultiProcessing
A cellular life simulation written in Python that uses both serial and parallel computation to parse a matrix over 100 iterations. To simulate changing cell states, the project uses intricate rule-based transformations using powers of two, prime numbers, and Fibonacci numbers. By dividing computing over several processes, it makes use of Python's multiprocessing module to increase performance. Concepts in concurrency, parallel processing, and performance optimization are illustrated in this project.

# Input & Output
Input:
The program accepts an input file containing a 2D matrix of characters that represent the initial state of the simulation. Each cell is defined by a single symbol:

O → Healthy O cell

o → Weakened O cell

X → Healthy X cell

x → Weakened X cell

. → Dead cell

The matrix is stored as plain text with no delimiters between characters, and each row is separated by a new line. This file represents time step 0 of the simulation.

Output:
After processing 100 iterations, the program writes the final state of the matrix to an output file. The output format matches the input format exactly:

Same row/column structure

Same symbol representation

No extra characters or formatting

The output file represents the state of the system at time step 100.
