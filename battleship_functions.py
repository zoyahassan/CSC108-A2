"""Battleship Functions"""

# Use these constants in your code
from typing import TextIO, List

MIN_SHIP_SIZE = 1
MAX_SHIP_SIZE = 10
MAX_GRID_SIZE = 10
UNKNOWN = "-"
EMPTY = "."
HIT = "X"
MISS = "M"


def read_ship_data(game_file: TextIO) -> List:
    """
    Return a list containing the ship characters in game_file as a list
    of strings at index 0, and ship sizes in game_file as a list of ints
    at index 1.
    """

    ship_characters = game_file.readline().split()

    ship_sizes = game_file.readline().split()

    for i in range(len(ship_sizes)):
        ship_sizes[i] = int(ship_sizes[i])

    return [ship_characters, ship_sizes]


##################################################
# Write the rest of the required functions here,
# following the function design recipe
##################################################


def is_valid_cell(row: int, col: int, grid_size: int) -> bool:
    """ 
    Return whether a cell with row and col exists in a grid with size 
    grid_size.
    
    >>> is_valid_cell(0, 1, 3) 
    True
    >>> is_valid_cell(3, 4, 2)
    False
    """ 
    
    return row < grid_size and col < grid_size
    

def is_not_given_char(row: int, col: int, grid: List[List[str]], 
                      ships: str) -> bool: 
    """  
    Return True iff the cell with row and col in the grid is not the same as
    the character ships. 
    
    >>> is_not_given_char(0, 1, [['a', '.'], ['.', 'b']], 'a') 
    True
    >>> is_not_given_char(0, 0, [['a', '.'], ['.', 'b']], 'a')
    False
    """
    
    return not grid[row][col] == ships
   

def has_ship(fleet_grid: List[List[str]], row: int, col: int, ships: str, 
             sizes: int) -> bool: 
    """
    Return True iff ships appears with the correct size, sizes, with the top or 
    left conrer of the ship starting at the given row and col, and completely in
    a row or in a column. 
    
    >>> has_ship([['a', '.'], ['a', '.']], 0, 0, 'a', 2)
    True
    >>> has_ship([['.', 'b', 'b'], ['a', '.', '.'], ['a', '.', '.']], 1, 1, \
    'a', 2)
    False
    """ 
    
    # check if the row and col is even in the fleet_grid, by calling to above 
    # function is_valid_cell 
    grid_size = len(fleet_grid)
    if not is_valid_cell(row, col, grid_size):
        return False 
    
    # check if the fleet_grid at the given row and col is equal to the 
    # ship_character, make call to above function is_not_given_char
    if is_not_given_char(row, col, fleet_grid, ships):
        return False 
    
    # check if the ship_character appears in the fleet_grid the same number of 
    # times as the size_of_ship
    char_count = 0 
    for i in fleet_grid:
        for j in i: 
            if j == ships:
                char_count = char_count + 1
    
    if not char_count == sizes: 
        return False 

    # check if the ship runs entirely in a row or col, w/o any index errors
    k = 1 
    while k < sizes:
        if (is_valid_cell(row, col + k, grid_size)) and \
           (is_valid_cell(row + k, col, grid_size)): 
            if (fleet_grid[row][col + k] != ships) and \
               (fleet_grid[row + k][col] != ships): 
                return False
        elif (is_valid_cell(row, col + k, grid_size)) and \
             not (is_valid_cell(row + k, col, grid_size)):
            if fleet_grid[row][col + k] != ships: 
                return False
        elif not (is_valid_cell(row, col + k, grid_size)) and \
             (is_valid_cell(row + k, col, grid_size)):
            if fleet_grid[row + k][col] != ships: 
                return False
        else: 
            return False 
        k = k + 1 
     
    return True 


def update_fleet_grid(row: int, col: int, fleet_grid: List[List[str]], 
                      ships: List[str], sizes: List[int], 
                      hits_list: List[int]) -> None:
    """ 
    The fleet_grid is updated to include an upper case letter of ships in 
    the row and col that it has been hit, and the hits_list is updated to 
    indicate that ships has been hit. If the number of hits is equal to the 
    size of the ship, sizes, then a message is printed. 
    
    >>> hits_list = [0, 0]
    >>> fleet_grid = [['a', 'a'], ['b', '.']] 
    >>> update_fleet_grid(0, 1, fleet_grid, ['a', 'b'], [2, 1], hits_list)
    >>> hits_list 
    [1, 0]
    >>> fleet_grid 
    [['a', 'A'], ['b', '.']]
    
    >>> hits_list = [0, 0] 
    >>> fleet_grid = [['b', 'a'], ['.', 'a']]
    >>> update_fleet_grid(0, 0, fleet_grid, ['a', 'b'], [2, 1], hits_list)
    The size 1 b ship has been sunk!
    >>> hits_list 
    [0, 1]
    >>> fleet_grid 
    [['B', 'a'], ['.', 'a']]
    """
    
    # add a hit on the hits_list, corresponding to the ship that was hit
    hits_list[ships.index(fleet_grid[row][col])] = hits_list[
        ships.index(fleet_grid[row][col])] + 1
    
    # if the number of hits on a ship is the same as the size of the ship, then
    # a call to print_sunk_message is made to indicate that the ship has sunk
    if hits_list[ships.index(fleet_grid[row][col])] == \
       sizes[ships.index(fleet_grid[row][col])]:
        print_sunk_message(sizes[ships.index(fleet_grid[row][col])], \
                           ships[ships.index(fleet_grid[row][col])])
        
    fleet_grid[row][col] = fleet_grid[row][col].upper()


def update_target_grid(row: int, col: int, target_grid: List[List[str]], 
                       fleet_grid: List[List[str]]) -> None:
    """
    Update the target_grid to HIT or MISS on the cell specfied by the row and 
    col, using the corresponding cell from fleet_grid.
    
    >>> fleet_grid = [['b', 'a'], ['.', 'a']]
    >>> target_grid = [['-', '-'], ['-', '-']]
    >>> update_target_grid(0, 0, target_grid, fleet_grid)
    >>> target_grid 
    [['X', '-'], ['-', '-']]
    
    >>> fleet_grid = [['b', 'a'], ['.', 'a']]
    >>> target_grid = [['-', '-'], ['-', '-']]
    >>> update_target_grid(1, 0, target_grid, fleet_grid)
    >>> target_grid 
    [['-', '-'], ['M', '-']]
    """
    
    if fleet_grid[row][col] != EMPTY:
        target_grid[row][col] = HIT 
    else: 
        target_grid[row][col] = MISS
    

    
def is_win(sizes: List[int], hits_list: List[int]) -> bool:
    """
    Return True iff all sizes is the same as hits_list, where all ships have 
    been sunk. 
    
    >>> is_win([2, 3], [2, 3]) 
    True
    >>> is_win([2, 3], [2, 2])
    False
    """
    
    return sizes == hits_list
    

def validate_character_count(fleet_grid: List[List[str]], ships: List[str], 
                             sizes: List[int]) -> bool: 
    """
    Return True iff fleet_grid contains the correct number of characters from 
    ships corresponding to sizes, and has the correct number of EMPTY 
    characters. 
    
    >>> validate_character_count([['a', '.'], ['a', '.']], ['a'], [2])
    True
    >>> validate_character_count([['.', '.'], ['a', '.']], ['a'], [2])
    False
    """    
    
    new_list = []
    total_empty_chars = 0 
    for lists in fleet_grid:
        for i in lists: 
            if i != '.': 
                new_list.append(i) 
            else: 
                total_empty_chars = total_empty_chars + 1 
    
    # make another list listing the # of times each char appears in fleet_grid
    count_chars = [] 
    for chars in ships: 
        count_chars.append(new_list.count(chars)) 
        
    total_chars = 0 
    for num in count_chars: 
        total_chars = total_chars + num 
    
    return count_chars == sizes and (
        len(fleet_grid) ** 2 == total_chars + total_empty_chars) 


def validate_ship_positions(fleet_grid: List[List[str]], ships: List[str], 
                            sizes: List[int]) -> bool: 
    """
    Return True iff fleet_grid contains the characters from ships with their
    corresponding sizes, aligned in consecutive cells completely in a row or 
    column. 
    
    >>> validate_ship_positions([['a', 'a', 'b'], ['.', '.', 'b'], \
    ['.', '.', 'b']], ['a', 'b'], [2, 3]) 
    True
    >>> validate_ship_positions([['a', 'b', 'a'], ['a', 'b', '.'], \
    ['.', 'b', '.']], ['a', 'b'], [2, 3]) 
    False
    """
    
    list_chars = [] 
    for lists in fleet_grid:
        for chars in lists:
            list_chars.append(chars) 
    
    index_first_chars = [] 
    for chars in ships: 
        if chars in list_chars: 
            index_first_chars.append(list_chars.index(chars)) 
    
    # using the first char indices from index_first_chars, find what the row
    # and col of the chars would be in fleet_grid, and make a call to has_ship 
    for i in range(len(index_first_chars)):
        row = index_first_chars[i] // len(fleet_grid)
        col = index_first_chars[i] % len(fleet_grid) 
        if not has_ship(fleet_grid, row, col, ships[i], sizes[i]):
            return False 
  
    return True 
            
    
def validate_fleet_grid(fleet_grid: List[List[str]], ships: List[str], 
                        sizes: List[int]) -> bool: 
    """
    Return True iff fleet_grid is a valid grid given ships and sizes.
    
    >>> validate_fleet_grid([['a', 'a', 'a'], ['.', '.', 'b'], ['.', '.', \
    'b']], ['a', 'b'], [3, 2]) 
    True
    >>> validate_fleet_grid([['.', 'a', 'a'], ['b', 'a', 'a'], ['b', '.', \
    '.']], ['a', 'b'], [4, 2])
    False
    """
        
    return validate_ship_positions(fleet_grid, ships, sizes) and \
           validate_character_count(fleet_grid, ships, sizes)


##################################################
# Helper function to call in update_fleet_grid
# Do not change!
##################################################


def print_sunk_message(ship_size: int, ship_character: str) -> None:
    """
    Print a message telling player that a ship_size ship with ship_character
    has been sunk.
    """

    print("The size {0} {1} ship has been sunk!".format(ship_size, 
                                                        ship_character))


if __name__ == "__main__":
    import doctest
    
    # uncomment the line below to run the docstring examples
    doctest.testmod()
    "pass"
