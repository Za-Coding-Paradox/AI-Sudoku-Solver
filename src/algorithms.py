def revise(csp, xi, xj):
    """Makes variable xi arc-consistent with respect to xj."""
    revised = False
    for x in csp.domains[xi][:]:
        # If no value y in D_j allows (x,y) to satisfy the constraint
        if not any(x != y for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True
    return revised

def ac3(csp):
    """
    Arc Consistency Algorithm (AC-3).
    Prunes domains based on initial constraints before search begins.
    """
    queue = [(u, v) for u in csp.variables for v in csp.neighbors[u]]
    
    while queue:
        xi, xj = queue.pop(0)
        if revise(csp, xi, xj):
            # If domain is emptied, no solution exists
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def forward_checking(csp, var, value, assignment):
    """
    Temporarily reduces the domains of unassigned neighbors.
    Returns True if no neighbor domain becomes empty, False otherwise.
    """
    removals = []
    for neighbor in csp.neighbors[var]:
        if neighbor not in assignment:
            if value in csp.domains[neighbor]:
                csp.domains[neighbor].remove(value)
                removals.append((neighbor, value))
                if not csp.domains[neighbor]:
                    return False, removals
    return True, removals

def backtrack_search(csp):
    """Initializes the recursive backtracking process."""
    return backtrack({}, csp)

def backtrack(assignment, csp):
    """
    Recursive backtracking search with Forward Checking.
    """
    csp.backtrack_calls += 1
    
    # Base case: All 81 variables assigned
    if len(assignment) == 81:
        return assignment
    
    # Select unassigned variable using Minimum Remaining Values (MRV) heuristic
    unassigned = [v for v in csp.variables if v not in assignment]
    var = min(unassigned, key=lambda v: len(csp.domains[v]))
    
    for value in csp.domains[var]:
        if csp.is_consistent(var, value, assignment):
            assignment[var] = value
            
            # Apply Forward Checking
            consistent, removals = forward_checking(csp, var, value, assignment)
            
            if consistent:
                result = backtrack(assignment, csp)
                if result:
                    return result
            
            # Backtrack: Restore domains and unassign variable
            for n, v in removals:
                csp.domains[n].append(v)
            del assignment[var]
            
    csp.backtrack_failures += 1
    return None
