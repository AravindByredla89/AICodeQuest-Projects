
import random
import time


def introduce_game():
    print("=" * 50)
    print("          THE MYSTERY ESCAPE ROOM")
    print("=" * 50)
    print("You wake up in a mysterious room.")
    print("The door is locked, and a countdown has begun!")
    print("Find the secret code to escape.")
    print("You have 5 attempts. Good luck!")
    print("=" * 50)
    time.sleep(1)


def search_room():
    clues = [
        "A note on the table says: 'The first digit is 7.'",
        "A painting has a number written behind it: 3.",
        "An old clock is stopped at 9.",
        "A book contains a strange message: 'Numbers matter.'",
        "A drawer contains a note: 'The last digit is 4.'"
    ]

    print("\nYou search the room and discover some clues...")
    random.shuffle(clues)

    for clue in clues:
        print(f"[CLUE] {clue}")
        time.sleep(0.7)

    print("\nYou notice a keypad beside the locked door.")
    print("The code has 3 digits.")
    print("Combine the clues to figure out the correct code.")


def solve_puzzle():
    secret_code = "739"
    attempts = 5

    while attempts > 0:
        guess = input("\nEnter the 3-digit code: ").strip()

        if len(guess) != 3 or not guess.isdigit():
            print("Enter exactly 3 digits.")
            continue

        if guess == secret_code:
            print("\nThe keypad flashes GREEN!")
            print("CLICK! The door unlocks.")
            print("You escaped the room. Congratulations!")
            return True

        correct_digits = sum(
            1 for digit in set(guess)
            if digit in secret_code
        )

        attempts -= 1
        print("Wrong code! The door remains locked.")
        print(f"Your guess shares {correct_digits} distinct digit(s) with the code.")
        print(f"Attempts remaining: {attempts}")

    print("\nThe keypad locks you out!")
    print(f"For this demo, the secret code was {secret_code}.")
    return False


def main():
    introduce_game()

    while True:
        choice = input(
            "\nWhat would you like to do?\n"
            "1. Search the room\n"
            "2. Try the keypad\n"
            "3. Give up\n"
            "Choose an option: "
        ).strip()

        if choice == "1":
            search_room()
        elif choice == "2":
            if solve_puzzle():
                break
        elif choice == "3":
            print("You gave up. The mystery remains unsolved!")
            break
        else:
            print("Invalid choice. Select 1, 2, or 3.")

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
