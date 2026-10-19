
import time


def introduce_case():
    print("=" * 55)
    print("          DIGITAL DETECTIVE: THE MUSEUM HEIST")
    print("=" * 55)
    print("A priceless diamond disappeared from a museum last night.")
    print("Three people were inside the building.")
    print("Your mission: investigate the clues and identify the thief.")
    print("\nSuspects:")
    print("1. Alice - Museum curator")
    print("2. Bob   - Security guard")
    print("3. Carol - Art collector")
    print("=" * 55)


def collect_clues():
    clues = {
        "footprints": "Small muddy footprints were found near the window.",
        "security": "The security cameras were disabled at 10:15 PM.",
        "keycard": "The security room was accessed using Bob's keycard.",
        "witness": "A witness saw someone wearing a blue jacket.",
        "window": "The window was locked from the inside."
    }

    print("\nYou inspect the crime scene...")
    time.sleep(1)

    for name, description in clues.items():
        print(f"\n[CLUE: {name.upper()}]")
        print(description)
        time.sleep(0.6)

    print("\nInvestigation notes:")
    print("- Bob had access to the security room.")
    print("- Alice was wearing a blue jacket.")
    print("- Carol entered through the main entrance.")
    print("- The footprints do not match Carol's shoes.")


def question_suspects():
    suspects = {
        "1": {
            "name": "Alice",
            "statement": "I was cataloguing paintings in the east wing."
        },
        "2": {
            "name": "Bob",
            "statement": "I was checking the cameras at 10:15 PM."
        },
        "3": {
            "name": "Carol",
            "statement": "I left the museum before 10 PM."
        }
    }

    print("\n--- SUSPECT INTERROGATION ---")

    for number, suspect in suspects.items():
        print(f"\n{number}. {suspect['name']}")
        print(f'Statement: "{suspect["statement"]}"')

    print("\nEvidence suggests the thief needed access to the security room.")
    print("However, a keycard alone does not prove who stole the diamond.")

    while True:
        choice = input(
            "\nWho do you want to accuse? (1: Alice, 2: Bob, 3: Carol): "
        ).strip()

        if choice in suspects:
            return suspects[choice]["name"]

        print("Invalid choice. Enter 1, 2, or 3.")


def deliver_verdict(accused):
    print("\n" + "=" * 55)
    print("                  FINAL VERDICT")
    print("=" * 55)

    # This is a fictional game solution, not a real deduction.
    culprit = "Bob"

    if accused == culprit:
        print(f"You accused {accused}.")
        print("Correct! Bob stole the diamond in this fictional case.")
        print("The keycard evidence helped solve the mystery!")
    else:
        print(f"You accused {accused}, but that accusation was incorrect.")
        print(f"For this game's predetermined solution, the thief was {culprit}.")
        print("Remember: clues should support a verdict, not merely suggest one.")

    print("\nCase closed. Thanks for playing, detective!")


if __name__ == "__main__":
    introduce_case()
    collect_clues()
    suspect = question_suspects()
    deliver_verdict(suspect)
