# Aaron caroltin
# Algorithm to solve any suduko puzzle with diagonal rule
# Assignment No1 :: AI-ND March 2017

assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[a[0]+a[1] for a in zip(rows, cols)] , [a[0]+a[1] for a in zip(rows, cols[::-1])]]
#print(diag_units)
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

 

def naked_twin_strategy(values, unitboxes, twinboxes, tofind):
    """
    For the given digits in twins, find & replace those digits among other boxes in same unit
    """
    #for box in unitboxes if len(values[box]) > 1 and box not in twinboxes:
    for box in unitboxes:
        if len(values[box]) > 1:
            if box not in twinboxes:
                for digit in tofind:
                    old_val = values[box]
                    new_val = old_val.replace(digit,'')
                    if new_val!=old_val:
                        values=assign_value(values, box, new_val)

    return values

def get_twinboxes(values, unitboxes, firstbox):
    """
    This function finds the secondbox (twin) of firstbox having the same vaule and if found, then returns them both
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        unitboxes: a list of boxes within the same uit as that of firstbox
        firstbox: This is a 2-digit box, for which we wish to find a twin.

    Returns:
        the list with twins or empty (f no twin found).
    """
    twins = [firstbox]
    val = values[firstbox]
    #for box in unitboxes if firstbox != box and values[box] == val:
    for box in unitboxes:
        if firstbox != box:
            if values[box] == val:
                twins.append(box)
        
    if len(twins) == 2:
        return twins
    else:
        return []

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # ddbox-doubledigit box
    # Narrow the initial search to finding ddboxes in puzzle and for each of them, 
    # start searching through all 3 units (row, col, box units)

    ddboxes = [box for box in values.keys() if len(values[box]) == 2]
    for ddbox in ddboxes:
        ddvalue =values[ddbox]
        ddboxunits = units[ddbox]
        for ddboxunit in ddboxunits:
            twinboxes = get_twinboxes(values,ddboxunit,ddbox)
            if(len(twinboxes) == 2):
                #found exactly one twin within this unit, so start naked twin strategy
                values = naked_twin_strategy(values, ddboxunit, twinboxes, ddvalue)
            
    return values   

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    #assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    Removes the digits from peers if already that digit has been assigned to a box in that peer list.
    Args:
        the values dictionary to which eliminate strategy to be performed.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            new_val = values[peer].replace(digit,'')
            values=assign_value(values, peer, new_val)
            
    return values

def only_choice(values):
    """
    Assigns the only possible value to the box if remaining boxes in that unit cannot have it.
    Args:
        the values dictionary on which the only_choice strategy to be performed.
    """

    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                #values[dplaces[0]] = digit
                values=assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Function to perform all strategies, till solution is found.
    Args:
        the values dictionary on which the reduce_puzzle strategy to be performed.
        returns False if no changes made to underlying puzle [dead end]
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        box_un = [box for box in values.keys() if len(values[box]) == 0]
        if len(box_un):
            return False
    return values

def search(values):
    """
    A recursive function that starts the search by finding a 2-digit box (or least available digit box)
     and start Recursive function to perform all strategies, till solution is found.
    Args:
        the values dictionary that is either solved or False when no solution found.
    """

    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))  
    

if __name__ == '__main__':
    #simple_sudoku_grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    #harder_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    display(solve(diag_sudoku_grid))
    

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
