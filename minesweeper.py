import functions

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

    >>> is_valid((4,4),4,[])
    False
    >>> is_valid((1,2),4,[(1,2)])
    False
    >>> is_valid(0,1),4,[])
    True
    """

    (row, col) = position

    if row < 0 or row >= size or col < 0 or col >= size or (row,col) in moves:
        return False
    return True

def game(size = 8, bombs = 8):
    """ Starts a game until all non-bomb positions are uncovered or until you find a bomb. """

    board = functions.assign_values(functions.make_board(size, bombs))
    moves = []
    print('Hi. Welcome to Minesweeper.:)')
    while True:
        functions.print_board(functions.visible_board(board, moves))
        position = input_position()
        if is_valid(position, size, moves):
            if board[position[0]][position[-1]] == '*':
                functions.print_board(board)
                print('Sorry. Game over:(')
                break
            functions.dig(board, moves, position)
            if len(moves) == (size**2 - bombs):
                functions.print_board(functions.visible_board(board, moves))
                print('Congratulations, you won!:)')
                break
        else: print('Invalid location. Try again.')