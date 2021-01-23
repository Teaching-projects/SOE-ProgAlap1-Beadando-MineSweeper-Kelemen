import random

def make_board(size:int, bombs:int) -> list:
    """ Creates board and places bombs randomly. 
    
    Args:
        size (int): the size of the board 
        bombs (int): the number of bombs
    Returns:
        list: contains the bombs
    """

    board = [[None for i in range (size)] for i in range (size)]

    bombs_planted = 0

    while bombs_planted < bombs:
        row = random.randint(0, size-1)
        col = random.randint(0, size-1)
        if board[row][col] != '*':
            board[row][col] = '*'
            bombs_planted += 1
    return board

def assign_values(board:list) -> list:
    """ Assigns a value to each position based on the number of neighboring bombs. 
    
    Args:
        board (list): contains the bombs
    Returns:
        list: contains the values and the bombs
    """

    for row in range (len(board)):
        for col in range (len(board)):
            if board[row][col] != '*': 
                board[row][col] = get_num_neighboring_bombs(board, row, col)
    return board 

def get_num_neighboring_bombs(board:list, row, col) -> int:
    """ Returns the number of neighboring bombs. 
    
    Args:
        board (list): contains the bombs
        row, col (int): the position to be checked
    Returns:
        int: the number of neighboring bombs
    """

    neighboring_bombs = 0

    for i in range(max(0, row-1), min(len(board)-1, row+1)+1):
        for j in range(max(0, col-1), min(len(board)-1, col+1)+1):
            if i == row and j == col: continue
            if board[i][j] == '*': neighboring_bombs += 1
    return neighboring_bombs

def input_position() -> tuple:
    """ Reads a position from the input and returns it. 
    
    Returns:
        tuple: a `(row,col)` pair of coordinates 
    """

    user_input = input('Where would you like to dig? Input as row, col: ').split(',')
    row = int(user_input[0])
    col = int(user_input[-1])
    return (row,col)

def is_valid(position:tuple, size:int, moves:list) -> bool:
    """ Checks if the position is already taken or not and checks if it's inside the board. 
    
    Args:
        position (tuple): a `(row,col)` pair of coordinates 
        size (int): the size of the board 
        moves (list): the current state of the game
    Returns:
        bool: `False` if the position is already taken, `True` otherwise
    """

    (row, col) = position

    if row < 0 or row >= size or col < 0 or col >= size or (row,col) in moves:
        print('Invalid location. Try again.')
        return False
    return True

def dig(board:list, moves:list, position:tuple) -> None:
    """ If you dig at a location with neighboring bombs, it finishes digging. If you dig at a location with no neighboring bombs, recursively digs neighbors. 
    
    Args:
        board (list): contains the values and the bombs
        moves (list): the current state of the game
        position (tuple): a `(row,col)` pair of coordinates 
    """

    (row,col) = position

    if board[row][col] > 0 and (row,col) not in moves:
        moves.append((row,col))

    if board[row][col] == 0:
        for r in range(max(0, row-1), min(len(board)-1, row+1)+1):
            for c in range(max(0, col-1), min(len(board)-1, col+1)+1):
                if (r, c) in moves: continue 
                else: moves.append((r,c))
                dig(board,moves,(r,c))
                 
def visible_board(board:list, moves:list) -> list:
    """ Creates a new board that represents what the user would see. 
    
    Args:
        board(list): contains the values and the bombs
        moves(list): the current state of the game
    Returns:
        list: contains the values based on the current state of the game
    """

    visible_board = [[None for i in range (len(board))] for i in range (len(board))]
    
    for row in range (len(board)):
        for col in range (len(board)):
            if (row,col) in moves:
                visible_board[row][col] = str(board[row][col])
            else: visible_board[row][col] = '□'
    return visible_board

def print_board(board:list) -> None:
    """ Prints out the board in a simple way. 
    
    Args:
        board(list): contains the values and the bombs
    """

    print()
    for row in range (len(board)):
        if row == 0:
            print(' ' * 3, end = ' ')
            for i in range (len(board)):
                print(i, end = ' ') 
            print()
            print()
        for col in range (len(board)):
            if col == 0:
                print(row,  end = '   ')
            print(board[row][col], end = ' ')
        print()
    print()

def game(size = 8, bombs = 8):
    """ Starts a game until all non-bomb positions are uncovered or until you find a bomb. """

    board = assign_values(make_board(size, bombs))
    moves = []
    print('Hi. Welcome to Minesweeper.:)')
    while True:
        print_board(visible_board(board, moves))
        position = input_position()
        if is_valid(position, size, moves):
            if board[position[0]][position[-1]] == '*':
                print_board(board)
                print('Sorry. Game over:(')
                break
            dig(board, moves, position)
            if len(moves) == (size**2 - bombs):
                print_board(visible_board(board, moves))
                print('Congratulations, you won!:)')
                break