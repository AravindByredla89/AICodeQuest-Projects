
import random
import time


def display_intro():
    print("=" * 50)
    print("       CYBER VAULT: SYSTEM INFILTRATION")
    print("=" * 50)
    print("Welcome, agent.")
    print("Your mission is to unlock the fictional cyber vault.")
    print("Complete three challenges to retrieve the secret.")
    print("=" * 50)


def scan_system():
    print("\n[SCANNING] Searching fictional network...")
    time.sleep(1)
    systems = ["FIREWALL-07", "NODE-142", "VAULT-900", "SERVER-X"]
    random.shuffle(systems)

    for system in systems:
        print(f"[FOUND] {system}")
        time.sleep(0.4)

    print("\nScan complete. Three challenges are available.")
    print("Hint: The password is a number between 10 and 99.")


def solve_challenges():
    score = 0

    # Challenge 1: Guess the number
    secret_number = random.randint(10, 99)
    print("\n--- CHALLENGE 1: PASSWORD CRACK ---")
    print("Guess the secret two-digit number.")

    for attempt in range(1, 5):
        try:
            guess = int(input(f"Attempt {attempt}/4: "))
        except ValueError:
            print("Enter a valid number.")
            continue

        if guess == secret_number:
            print("Password accepted!")
            score += 1
            break
        elif guess < secret_number:
            print("Hint: The number is higher.")
        else:
            print("Hint: The number is lower.")

    if score == 0:
        print(f"Challenge failed. The number was {secret_number}.")

    # Challenge 2: Logic puzzle
    print("\n--- CHALLENGE 2: LOGIC GATE ---")
    print("What comes next in the sequence?")
    print("2, 4, 8, 16, ?")

    answer = input("Your answer: ").strip()
    if answer == "32":
        print("Logic gate unlocked!")
        score += 1
    else:
        print("Incorrect. The answer was 32.")

    # Challenge 3: Decryption
    print("\n--- CHALLENGE 3: MESSAGE DECRYPTION ---")
    encrypted = "Uifsf jt b tfdsfu"
    print(f"Encrypted message: {encrypted}")
    print("Hint: Every letter has been shifted forward by one.")

    answer = input("Decrypted message: ").strip().lower()
    if answer == "there is a secret":
        print("Message decrypted successfully!")
        score += 1
    else:
        print("Incorrect. The message was: there is a secret")

    return score


def show_results(score):
    print("\n" + "=" * 50)
    print("             MISSION REPORT")
    print("=" * 50)
    print(f"Challenges completed: {score}/3")

    if score == 3:
        print("ACCESS GRANTED! You are a cyber intelligence expert.")
        print("SECRET FILE: Project Nightfall has been recovered.")
    elif score >= 1:
        print("PARTIAL ACCESS. Some vault sections remain locked.")
    else:
        print("ACCESS DENIED. Training is recommended.")

    print("=" * 50)
    print("Simulation complete. No real systems were accessed.")


if __name__ == "__main__":
    display_intro()
    scan_system()
    final_score = solve_challenges()
    show_results(final_score)
