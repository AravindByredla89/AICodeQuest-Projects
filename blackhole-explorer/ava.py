
board = [" " for _ in range(9)]


def display_board():
    print()
    for i in range(0, 9, 3):
        print(" " + " | ".join(board[i:i + 3]))
        if i < 6:
            print("---+---+---")
    print()


def check_win(player):
    winning_combinations = [
        (0, 1, 2),  # Rows
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),  # Columns
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),  # Diagonals
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] == player:
            return True

    return False


def play_game():
    # Display positions for reference
    print("Welcome to Criss-Cross!")
    print("Player 1: X | Player 2: O")
    print("Choose a position from 1 to 9.")

    for i in range(9):
        display_board()
        player = "X" if i % 2 == 0 else "O"

        while True:
            try:
                move = int(input(f"Player {player}, enter position: "))

                if move < 1 or move > 9:
                    print("Enter a number between 1 and 9.")
                elif board[move - 1] != " ":
                    print("Position already occupied. Try again.")
                else:
                    board[move - 1] = player
                    break

            except ValueError:
                print("Please enter a valid integer.")

        if check_win(player):
            display_board()
            print(f"Player {player} wins!")
            return

    display_board()
    print("It's a draw!")


play_game()
