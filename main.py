import sys
import os
from src.csp import SudokuCSP
from src.algorithms import ac3, backtrack_search

def print_board(assignment):
    """Prints the assigned Sudoku board in a clean 9x9 grid."""
    print("-" * 13)
    for r in range(9):
        line = "|"
        for c in range(9):
            line += str(assignment[(r, c)])
            if (c + 1) % 3 == 0:
                line += "|"
        print(line)
        if (r + 1) % 3 == 0:
            print("-" * 13)

def solve_board(file_path):
    """Reads file, initializes CSP, runs AC-3 and Backtracking."""
    print(f"\nProcessing: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            board_text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        csp = SudokuCSP(board_text)
    except ValueError as e:
        print(f"Error initializing board: {e}")
        return

    # Step 1: Preprocessing with AC-3
    print("Running AC-3 inference...")
    if not ac3(csp):
        print("AC-3 determined this board has no solution based on initial constraints.")
        return

    # Step 2: Search
    print("Executing Backtracking Search with Forward Checking...")
    solution = backtrack_search(csp)

    if solution:
        print("\nSolution Found:")
        print_board(solution)
        print("\n--- Performance Metrics ---")
        print(f"Backtrack Calls:    {csp.backtrack_calls}")
        print(f"Backtrack Failures: {csp.backtrack_failures}")
        print("---------------------------\n")
    else:
        print("\nNo solution exists for this board.")
        print(f"Backtrack Calls: {csp.backtrack_calls}")
        print(f"Backtrack Failures: {csp.backtrack_failures}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_sudoku_file>")
        print("Example: python main.py data/easy.txt")
    else:
        file_path = sys.argv[1]
        solve_board(file_path)
