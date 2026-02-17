import json
import os
import random
import time
import threading

# Directory to store JSON files
QUIZ_DIR = "quiz_categories"

# Ensure the directory exists
os.makedirs(QUIZ_DIR, exist_ok=True)

def get_category_file(category):
    """Return the file path for a given category."""
    return os.path.join(QUIZ_DIR, f"{category.lower()}.json")

def load_questions(category):
    """Load questions from a JSON file."""
    file_path = get_category_file(category)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return []

def save_questions(category, questions):
    """Save questions to a JSON file."""
    file_path = get_category_file(category)
    with open(file_path, "w") as file:
        json.dump(questions, file, indent=4)

def add_category():
    """Add a new category."""
    category = input("Enter the name of the new category: ").strip()
    if os.path.exists(get_category_file(category)):
        print("Category already exists.")
    else:
        save_questions(category, [])
        print(f"Category '{category}' created.")

def add_question():
    """Add a new question and answer."""
    category = input("Enter the category for the question: ").strip()
    if not os.path.exists(get_category_file(category)):
        print(f"Category '{category}' does not exist. Please create it first.")
        return

    questions = load_questions(category)

    question = input("Enter the question: ").strip()
    answer = input("Enter the answer: ").strip()

    questions.append({"question": question, "answer": answer})
    save_questions(category, questions)
    print("Question added.")

def wait_or_skip():
    """Wait 7 seconds or skip if Enter is pressed."""
    skip_event = threading.Event()

    def wait_for_enter():
        input()  # Wait for Enter key
        skip_event.set()

    threading.Thread(target=wait_for_enter, daemon=True).start()

    for _ in range(7):
        if skip_event.is_set():
            return True  # Skip triggered
        time.sleep(1)

    return False  # Timeout reached

def start_quiz():
    """Start the quiz."""
    categories = [f[:-5].capitalize() for f in os.listdir(QUIZ_DIR) if f.endswith(".json")]
    if not categories:
        print("No categories available.")
        return

    print("Available categories:")
    for i, category in enumerate(categories, 1):
        print(f"{chr(96+i)}. {category}")
    print(f"{chr(96+len(categories)+1)}. All categories combined")

    choice = input(f"Choose a category (a-{chr(96+len(categories)+1)}): ").strip().lower()

    if choice == chr(96+len(categories)+1):
        selected_questions = []
        for category in categories:
            selected_questions.extend(load_questions(category))
    else:
        try:
            category = categories[ord(choice) - 97]
            selected_questions = load_questions(category)
        except (IndexError, ValueError):
            print("Invalid choice.")
            return

    if not selected_questions:
        print("No questions in the selected category.")
        return

    random.shuffle(selected_questions)
    print("Starting the quiz. Press CTRL+C to quit. Press Enter to see the answer or skip to the next question.")
    try:
        for qa in selected_questions:
            print(f"Question: {qa['question']}")

            skipped = wait_or_skip()

            print(f"Answer: {qa['answer']}")
            print("-")
    except KeyboardInterrupt:
        print("\nQuiz interrupted. Returning to the main menu.")

def main():
    """Main loop."""
    while True:
        print("\nKnowledge Quiz")
        print("1. Add a new category")
        print("2. Add a new question")
        print("3. Start the quiz")
        print("4. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_category()
        elif choice == "2":
            add_question()
        elif choice == "3":
            start_quiz()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Preload default categories with sample questions
    default_categories = {
        "Linux": [
            {"question": "What command is used to list files in Linux?", "answer": "ls"},
            {"question": "What is the default shell in most Linux distributions?", "answer": "bash"}
        ],
        "Python": [
            {"question": "What keyword is used to define a function in Python?", "answer": "def"},
            {"question": "What is Python's standard package manager?", "answer": "pip"}
        ],
        "Chess": [
            {"question": "How many squares are on a chessboard?", "answer": "64"},
            {"question": "What is the term for a move that puts the king in check and cannot be stopped?", "answer": "Checkmate"}
        ],
        "Geography": [
            {"question": "What is the capital of France?", "answer": "Paris"},
            {"question": "Which continent is the Sahara Desert located on?", "answer": "Africa"}
        ],
        "Electronics": [
            {"question": "What does LED stand for?", "answer": "Light Emitting Diode"},
            {"question": "What is the unit of electrical resistance?", "answer": "Ohm"}
        ]
    }

    for category, questions in default_categories.items():
        if not os.path.exists(get_category_file(category)):
            save_questions(category, questions)

    main()

