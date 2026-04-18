class SudokuCSP:
    """
    Represents the Sudoku board as a Constraint Satisfaction Problem.
    Tracks variables, domains, neighbors, and performance metrics.
    """
    def __init__(self, board_text):
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        self.neighbors = {v: set() for v in self.variables}
        
        # Performance metrics tracking
        self.backtrack_calls = 0
        self.backtrack_failures = 0
        
        self._initialize_domains(board_text)
        self._initialize_neighbors()

    def _initialize_domains(self, board_text):
        """Parses the 9x9 text grid and sets initial domains."""
        lines = board_text.strip().split('\n')
        if len(lines) != 9:
            raise ValueError("Board must have exactly 9 lines.")
            
        for r in range(9):
            line = lines[r].strip()
            if len(line) != 9:
                raise ValueError(f"Line {r+1} does not have exactly 9 digits.")
                
            for c in range(9):
                val = int(line[c])
                if val == 0:
                    self.domains[(r, c)] = list(range(1, 10))
                else:
                    self.domains[(r, c)] = [val]

    def _initialize_neighbors(self):
        """Defines the row, column, and 3x3 box constraints for each cell."""
        for r, c in self.variables:
            # Row and Column constraints
            for i in range(9):
                if i != c: self.neighbors[(r, c)].add((r, i))
                if i != r: self.neighbors[(r, c)].add((i, c))
                
            # 3x3 Box constraints
            box_row, box_col = 3 * (r // 3), 3 * (c // 3)
            for i in range(box_row, box_row + 3):
                for j in range(box_col, box_col + 3):
                    if (i, j) != (r, c):
                        self.neighbors[(r, c)].add((i, j))

    def is_consistent(self, var, value, assignment):
        """Checks if assigning a value violates any constraints with current neighbors."""
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True
