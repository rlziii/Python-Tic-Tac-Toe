from enum import Enum
import random
import sys

# Enums

class Color(Enum):
    NONE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6

class BoardType(Enum):
    SIMPLE = "-simple"
    NUMBERED = "-numbered"

class Piece(Enum):
    X = "X"
    O = "O"
    E = " "

# Functions

def color_str(color, string):
    esc_code = "\N{ESC}"
    color_code = "[3" + str(color.value) + "m"
    none_code = "[" + str(Color.NONE.value) + "m"
    return esc_code + color_code + string + esc_code + none_code

def space_for_index(index, board_array):
    space = board_array[index]
    if space == Piece.E:
        return color_str(Color.YELLOW, str(index + 1))
    else:
        return color_str(Color.RED, space.value)

def print_numbered_board(board_array):
    print()
    print(space_for_index(0, board_array) + "|" + space_for_index(1, board_array) + "|" + space_for_index(2, board_array))
    print("-----")
    print(space_for_index(3, board_array) + "|" + space_for_index(4, board_array) + "|" + space_for_index(5, board_array))
    print("-----")
    print(space_for_index(6, board_array) + "|" + space_for_index(7, board_array) + "|" + space_for_index(8, board_array))
    print()

def print_simple_board(board_array):
    print()
    print(board_array[0].value + "|" + board_array[1].value + "|" + board_array[2].value)
    print("-----")
    print(board_array[3].value + "|" + board_array[4].value + "|" + board_array[5].value)
    print("-----")
    print(board_array[6].value + "|" + board_array[7].value + "|" + board_array[8].value)
    print()

def print_board(board_type, board_array):
    if board_type == BoardType.SIMPLE:
        print_simple_board(board_array)
    elif board_type == BoardType.NUMBERED:
        print_numbered_board(board_array)
    else:
        raise ValueError(f"Invalid board type: {board_type}")

def create_board_array():
    return [Piece.E, Piece.E, Piece.E, Piece.E, Piece.E, Piece.E, Piece.E, Piece.E, Piece.E]

def check_spaces_for_winner(board_array, first_index, second_index, third_index):
    return board_array[first_index] != Piece.E and board_array[first_index] == board_array[second_index] == board_array[third_index]

def check_for_winner(board_array, print_results=False):
    isWinner = False
    winningPlayer = Piece.E

    # Top horizontal.
    if check_spaces_for_winner(board_array, 0, 1, 2):
        isWinner = True
        winningPlayer = board_array[0]
    # Middle horizontal.
    elif check_spaces_for_winner(board_array, 3, 4, 5):
        isWinner = True
        winningPlayer = board_array[3]
    # Bottom horizontal.
    elif check_spaces_for_winner(board_array, 6, 7, 8):
        isWinner = True
        winningPlayer = board_array[6]
    # Left vertical.
    elif check_spaces_for_winner(board_array, 0, 3, 6):
        isWinner = True
        winningPlayer = board_array[0]
    # Middle vertical.
    elif check_spaces_for_winner(board_array, 1, 4, 7):
        isWinner = True
        winningPlayer = board_array[1]
    # Right vertical.
    elif check_spaces_for_winner(board_array, 2, 5, 8):
        isWinner = True
        winningPlayer = board_array[2]
    # Main diagonal (\).
    elif check_spaces_for_winner(board_array, 0, 4, 8):
        isWinner = True
        winningPlayer = board_array[0]
    # Minor diagonal (/).
    elif check_spaces_for_winner(board_array, 2, 4, 8):
        isWinner = True
        winningPlayer = board_array[2]
    
    if isWinner and winningPlayer != Piece.E and print_results:
        print(f"Player {winningPlayer.value} won the game!")

    return isWinner

def check_for_tie(board_array, print_results=False):
    isTie = len([x for x in board_array if x == Piece.E]) == 0

    if isTie and print_results:
        print("It's a tie!")

    return isTie

def random_empty_space_index(board_array):
    empty_spaces = [(index, element) for (index, element) in list(enumerate(board_array)) if element == Piece.E]
    random_empty_space = random.choice(empty_spaces)
    return random_empty_space[0]

def user_choice_prompt(board_array):
    position = 0

    while position == 0:
        user_input = input("Choose your position (1-9): ")
        try:
            user_input = int(user_input)
            if user_input < 1 or user_input > 9:
                raise ValueError("User input out of range.")
            elif board_array[user_input - 1] != Piece.E:
                print("Error: This space is not available.")
                continue
            else:
                position = user_input
        except ValueError:
            print("Error: Invalid input.")
            continue

    # Adjust for 0-based index.
    return position - 1

def user_turn(board_array):
    position = user_choice_prompt(board_array)
    board_array[position] = Piece.X

def computer_turn(board_array):
    position = random_empty_space_index(board_array)
    board_array[position] = Piece.O

def get_board_type():
    default = BoardType.NUMBERED

    if len(sys.argv) == 2:
        if sys.argv[1] == BoardType.SIMPLE.value:
            return BoardType.SIMPLE
        elif sys.argv[1] == BoardType.NUMBERED.value:
            return BoardType.NUMBERED
        else:
            return default
    else:
        return default

# Main

def main():
    board_type = get_board_type()
    play_game = True
    while play_game:
        board_array = create_board_array()
        game_is_over = False

        print_board(board_type, board_array)

        while not game_is_over:
            user_turn(board_array)
            game_is_over = check_for_winner(board_array) or check_for_tie(board_array)

            if not game_is_over:
                computer_turn(board_array)
                game_is_over = check_for_winner(board_array) or check_for_tie(board_array)

            print_board(board_type, board_array)

            if game_is_over:
                check_for_winner(board_array, print_results=True) or check_for_tie(board_array, print_results=True)

                print()
                play_again_user_input = input("Play again? (Y/n) ")
                if play_again_user_input != "" and play_again_user_input != "Y" and play_again_user_input != "y":
                    play_game = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print("Bye-bye!")
        quit()