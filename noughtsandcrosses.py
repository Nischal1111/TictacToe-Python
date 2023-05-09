import random
import os.path
import json
random.seed()


def draw_board(board):
    '''Prints the board in 3*3 matrix and the argument of board is passed from
    python_play_game.py '''
    # Creating the layout of the board.
    print("-------------")
    # [] on left is row,[] on right is column.
    print("|", board[0][0], "|", board[0][1], "|", board[0][2], "|")
    print("|---|---|---|")
    print("|", board[1][0], "|", board[1][1], "|", board[1][2], "|")
    print("|---|---|---|")
    print("|", board[2][0], "|", board[2][1], "|", board[2][2], "|")
    print("-------------")


def welcome(board):
    print("Welcome to the 'Unbeataible Noughts and Crossess' game .")
    print("The board layout is shown below")
    draw_board(board)
    print("When prompted,enter the number corresponding to the square you want.")


def initialise_board(board):
    '''This function helps to empty the space in the cell to initialize 
    the game of tic-tac-toe. 
    '''
    # i is the row in3*3 matrix.
    # Iterates through 1 row at a time until 3 rows are reached.
    for i in range(3):
        # j is the coloumn in 3*3 matrix
        # Iterates through 3 Columns in 1 row at a time until 9 ciolumns are reached.
        for j in range(3):
            # During the loop this sets value of boar[i][j]to an empty space to ensure the cell is unused.
            board[i][j] = ' '
    # returns the initialized board after iterating
    return board


def get_player_move(board):
    while True:
        try:
            print('\t\t\t\t1 2 3')
            print('\t\t\t\t4 5 6')
            print('\t\t\t\t7 8 9')
            move = int(input("Enter a cell number between (1-9) :"))
            if move < 1 or move > 9:
                raise ValueError("Invalid move.")
            row, col = (move-1)//3, (move-1) % 3
            if board[row][col] != " ":
                raise ValueError("Cell is already occupied.")
            return row, col
        except ValueError as error:
            print(error)
        except Exception as error:
            print("An error occurred:", error)
            raise error


def choose_computer_move(board):
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
    for row in board:
        if " " in row:
            return False
    return True


def play_game(board):
    initialise_board(board)
    draw_board(board)

    for i in range(9):
        row, col = get_player_move(board)
        board[row][col] = "X"
        if check_for_win(board, "X"):
            print("You have won the game!")
            draw_board(board)
            score = 1
            print(f"The score is {score}")
            return score
        if check_for_draw(board):
            print("The game ended in draw.")
            score = 0
            print(f"The score is {score}")
            return score
        row, col = choose_computer_move(board)
        board[row][col] = "0"
        draw_board(board)

        if check_for_win(board, "0"):
            print("You have lost the game!")
            draw_board(board)
            print(f"The score is {score}")
            score = -1
            return score


def menu():
    while True:
        print("1. Play the game")
        print("2. Save your score in the leaderboard")
        print("3. Load and display the leaderboard")
        print("q. quite the game")
        choice = input("Enter an input number between 1, 2, 3 or q: ")
        if choice in ['1', '2', '3', 'q']:
            return choice
        else:
            print("Invalid option.")


def save_score(score):
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
    for name, score in leaders.items():
        print(f"{name}: {score}")
