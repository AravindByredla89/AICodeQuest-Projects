import random


def display_welcome():
    print("=" * 45)
    print("         PYTHON QUIZ CHALLENGE")
    print("=" * 45)
    print("Answer the questions and test your knowledge!")
    print("Each correct answer earns 1 point.")
    print("-" * 45)


def get_questions():
    questions = [
        {
            "question": "Which keyword defines a function in Python?",
            "options": ["A. func", "B. def", "C. function", "D. define"],
            "answer": "B"
        },
        {
            "question": "Which data type stores True or False?",
            "options": ["A. int", "B. str", "C. bool", "D. list"],
            "answer": "C"
        },
        {
            "question": "What is the output of 3 ** 2?",
            "options": ["A. 6", "B. 9", "C. 8", "D. 5"],
            "answer": "B"
        },
        {
            "question": "Which symbol is used for comments?",
            "options": ["A. //", "B. <!--", "C. #", "D. **"],
            "answer": "C"
        },
        {
            "question": "Which method adds an item to a list?",
            "options": ["A. add()", "B. append()", "C. insert_end()", "D. push()"],
            "answer": "B"
        },
        {
            "question": "Which loop iterates over a sequence?",
            "options": ["A. for", "B. repeat", "C. loop", "D. iterate"],
            "answer": "A"
        },
        {
            "question": "What does len('Python') return?",
            "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
            "answer": "B"
        },
        {
            "question": "Which collection stores unique values?",
            "options": ["A. list", "B. tuple", "C. set", "D. string"],
            "answer": "C"
        }
    ]

    random.shuffle(questions)
    return questions


def conduct_quiz(questions):
    score = 0
    total_questions = len(questions)

    for index, question in enumerate(questions, start=1):
        print(f"\nQuestion {index}/{total_questions}")
        print(question["question"])

        for option in question["options"]:
            print(option)

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer in ["A", "B", "C", "D"]:
                break

            print("Invalid choice. Please enter A, B, C, or D.")

        if answer == question["answer"]:
            print("Correct answer!")
            score += 1
        else:
            print(f"Incorrect! The correct answer is {question['answer']}.")

        print("-" * 45)

    return score


def show_results(score, total):
    percentage = (score / total) * 100

    print("\n" + "=" * 45)
    print("               QUIZ RESULTS")
    print("=" * 45)
    print(f"Total questions : {total}")
    print(f"Correct answers : {score}")
    print(f"Wrong answers   : {total - score}")
    print(f"Final score     : {percentage:.2f}%")

    if percentage >= 80:
        print("Excellent work! You know your Python well.")
    elif percentage >= 50:
        print("Good effort! Keep practicing.")
    else:
        print("Keep learning. You will improve with practice.")

    print("=" * 45)


if __name__ == "__main__":
    display_welcome()
    quiz_questions = get_questions()
    final_score = conduct_quiz(quiz_questions)
    show_results(final_score, len(quiz_questions))
