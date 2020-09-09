import copy
import random


def drawBoard(board):
    # This function prints out the board that it was passed.

    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-+-+-')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-+-+-')
    print(board['bot-L'] + '|' + board['bot-M'] + '|' + board['bot-R'])


def inputPlayerLetter():
    # Allow the player to choose which letter they want to be.
    # Returns a list with the players selection as the first letter, and the computer's as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        letter = input('Do you want to be X or O? ').upper()

    # The first element in the list is the players letter, the second is the computers.
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    # Randomly choose whether player or computer goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(brd, let):
    # Given a board and a players letter, this function returns True if that player has won.
    # Used 'brd' instead of 'board' and 'let' instead of 'letter' to reduce typing.
    return ((brd['top-L'] == let and brd['top-M'] == let and brd['top-R'] == let) or  # Top-row (across)
            (brd['mid-L'] == let and brd['mid-M'] == let and brd['mid-R'] == let) or  # Mid-row (across)
            (brd['bot-L'] == let and brd['bot-M'] == let and brd['bot-R'] == let) or  # Bot-row (across)
            (brd['top-L'] == let and brd['mid-L'] == let and brd['bot-L'] == let) or  # Left-row (down)
            (brd['top-M'] == let and brd['mid-M'] == let and brd['bot-M'] == let) or  # Mid-row (down)
            (brd['top-R'] == let and brd['mid-R'] == let and brd['bot-R'] == let) or  # Right-row (down)
            (brd['top-L'] == let and brd['mid-M'] == let and brd['bot-R'] == let) or  # Diagonal (left-to-right)
            (brd['top-R'] == let and brd['mid-M'] == let and brd['bot-L'] == let))  # Diagonal (right-to-left)


def isSpaceFree(board, move):
    # Return True if the passed move is free on the passed board.
    return board[move] == ' '


def getPlayerMove(board):
    # Let the player type in his move.
    move = ' '
    while move not in 'top-L top-M top-R mid-L mid-M mid-R bot-L bot-M bot-R'.split() or not isSpaceFree(board, move):
        move = input('What is your next move? (top-, mid-, bot- & L, M, R): ')
    return move


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns none if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getComputerMove(board, computerLetter):
    # Given a board and the computer's letter, determine where to move and return that move.
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # Here is the algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move.
    for i in 'top-L top-M top-R mid-L mid-M mid-R bot-L bot-M bot-R'.split():
        dupe = copy.copy(board)
        if isSpaceFree(dupe, i):
            makeMove(dupe, computerLetter, i)
            if isWinner(dupe, computerLetter):
                return i

    # Check if the player can win on his next move, and block them.
    for i in 'top-L top-M top-R mid-L mid-M mid-R bot-L bot-M bot-R'.split():
        dupe = copy.copy(board)
        if isSpaceFree(dupe, i):
            makeMove(dupe, playerLetter, i)
            if isWinner(dupe, playerLetter):
                return i

    # Try to take one of the corners if they are free.
    move = chooseRandomMoveFromList(board, ['top-L', 'top-R', 'bot-L', 'bot-R'])
    if move is not None:
        return move

    # If free, try to take the center.
    if isSpaceFree(board, 'mid-M'):
        return 'mid-M'

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, ['top-M', 'bot-M', 'mid-L', 'mid-R'])


def isBoardFull(board):
    # Return true is every space on the board has been taken. Otherwise, return False.
    for i in 'top-L top-M top-R mid-L mid-M mid-R bot-L bot-M bot-R'.split():
        if isSpaceFree(board, i):
            return False
    return True


print('\nWelcome to Tic Tac Toe!\n')

while True:
    # Reset the board.
    theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ',
                'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ',
                'bot-L': ' ', 'bot-M': ' ', 'bot-R': ' '}

    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print(f'The {turn} will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            # Player's turn.
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('Well Done!! You have WON the game!!!\n')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print("This game is a tie, you'll get him next time!\n")
                    break
                else:
                    turn = 'computer'

        else:
            # Computers turn.
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('Unlucky!! The computer has beaten you! Better luck next time...\n')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print("This game is a tie, you'll get him next time!\n")
                    break
                else:
                    turn = 'player'

    if not playAgain():
        break
