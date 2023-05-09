import random
import os.path
import json
random.seed()


def draw_board(board):
    '''Prints the board in 3*3 matrix and the argument of board is passed from
    python_play_game.py '''
    # Making the layout of the tictactoe or noughtsandcrosses
    print("-------------")
    # [] on left is row,[] on right is column.
    print("|", board[0][0], "|", board[0][1], "|", board[0][2], "|")
    print("|---|---|---|")
    print("|", board[1][0], "|", board[1][1], "|", board[1][2], "|")
    print("|---|---|---|")
    print("|", board[2][0], "|", board[2][1], "|", board[2][2], "|")
    print("-------------")


def welcome(board):
    # This functions welcomes the user and displays the message and the board.
    print("Welcome to the 'Unbeataible Noughts and Crossess' game .")
    print("The board layout is shown below")
    draw_board(board)
    print("When prompted,enter the number corresponding to the square you want.")


def initialise_board(board):
    '''This function initializes the board and allows user to input value in the empty cells 
    '''
    # i is row of the board and is iterated to create a tictactoe structure and is a 3*3 matrix
    for i in range(3):
        # j is the coloumn of the board is iterated and is a 3*3 matrix
        for j in range(3):
            board[i][j] = ' '
    # Returning the empty board where user can put their input in later phase
    return board


def get_player_move(board):
    # this function asks user for input in the desired cell in tictactoe but are prompted to do again if cell occupied
    while True:
        try:
            # this allows user for greater understanding of the cell
            print('\t\t\t\t1 2 3')
            print('\t\t\t\t4 5 6')
            print('\t\t\t\t7 8 9')
            # asking user for cell numbers to put input
            move = int(input("Enter a cell number between (1-9) :"))
            if move < 1 or move > 9:
                raise ValueError("Invalid move.")
            row, col = (move-1)//3, (move-1) % 3
            if board[row][col] != " ":
                raise ValueError("Cell is already occupied.")
            return row, col
        except ValueError as error:  # Raising an error if user inputs a wrong value as input
            print(error)
        except Exception as error:
            print("An error occurred:", error)
            raise error


def choose_computer_move(board):
    # this function puts the computer input in the game
    while True:
        try:
            comp_move = random.randint(1, 9)
            row, col = (comp_move-1)//3, (comp_move-1) % 3
            if board[row][col] != " ":
                raise ValueError
            return row, col
        except Exception as error:
            print(error)


def check_for_win(board, mark):
    # this function checks for win after each move and checks horizontally, vertically, and diagonally.
    for row in board:
        if row.count(mark) == 3 and ' ' not in row:
            return True
    # Check columns
    for i in range(3):
        column = [row[i] for row in board]
        if column.count(mark) == 3 and ' ' not in column:
            return True
    # Check diagonals
    diagonal1 = [board[i][i] for i in range(3)]
    diagonal2 = [board[i][2-i] for i in range(3)]
    if diagonal1.count(mark) == 3 and ' ' not in diagonal1:
        return True
    if diagonal2.count(mark) == 3 and ' ' not in diagonal2:
        return True
    # No winning condition found
    return False


def check_for_draw(board):
    # this function checks for draws after checking for win is false
    for row in board:
        if " " in row:
            return False
    return True


def play_game(board):
    """this is the function where we run all the above function
    we run initialise_board and draw_board to display to the user and later we play the game
    as user inputs and computer generates the value.
    """
    initialise_board(board)
    draw_board(board)

    for i in range(9):
        row, col = get_player_move(board)
        board[row][col] = "X"
        if check_for_win(board, "X"):
            print("You have won the game!")
            draw_board(board)
            score = 1  # displaing score after each round
            print(f"The score is {score}")
            return score
        if check_for_draw(board):
            print("The game ended in draw.")
            score = 0  # displaing score after each round
            print(f"The score is {score}")
            return score
        row, col = choose_computer_move(board)
        board[row][col] = "0"
        draw_board(board)

        if check_for_win(board, "0"):
            print("You have lost the game!")
            draw_board(board)
            score = -1  # displaing score after each round
            print(f"The score is {score}")
            return score


def menu():
    # Asking user if they want to play game, save the score, load the score or quit the game
    while True:
        print("1. Play the game")
        print("2. Save your score in the leaderboard")
        print("3. Load and display the score leaderboard")
        print("q. Quit the game")
        choice = input("Enter an number between 1, 2, 3 or q: ")
        if choice in ['1', '2', '3', 'q']:
            return choice
        else:
            print("Invalid option.")


def save_score(score):
    # Saving the score by writing the data in the leaderboard.txt
    # asking user for name and appending it to the file
    name = input("Enter your name: ")
    score_in_leaderboard = {}
    filename = "leaderboard.txt"
    if is_file(filename):
        try:
            with open('leaderboard.txt', 'r') as f:
                score_in_leaderboard = json.load(f)
        except FileNotFoundError as e:
            raise e
        if name in score_in_leaderboard:
            score_in_leaderboard[name] = score+score_in_leaderboard[name]
        else:
            score_in_leaderboard[name] = score

        with open('leaderboard.txt', 'w') as f:
            json.dump(score_in_leaderboard, f)

        print("Score has been saved to leaderboard.")
    else:
        print("Sorry, Leaderboard not found")


def is_file(filename):
    # this function checks if file exists
    return os.path.exists(filename)


def load_scores():
    try:
        filename = "leaderboard.txt"
        if is_file(filename):
            with open('leaderboard.txt', 'r') as f:
                score_in_leaderboard = json.load(f)
                return score_in_leaderboard
        else:
            print("Leaderboard not found")
    except Exception as error:
        print(f"Error occurred while loading the scores: {error}")
        raise error


def display_leaderboard(leaders):
    # this function loads the score from the file
    for name, score in leaders.items():
        print(f"{name}: {score}")
