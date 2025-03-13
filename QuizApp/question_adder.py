import json
import os

# File path for storing questions
QUESTIONS_FILE = "quiz_questions.json"

# Load existing questions from the JSON file
def load_questions():
    """Load questions from the JSON file."""
    if not os.path.exists(QUESTIONS_FILE):
        return []  # Return an empty list if the file doesn't exist
    with open(QUESTIONS_FILE, "r") as file:
        return json.load(file)

# Save questions to the JSON file
def save_questions(questions):
    """Save questions to the JSON file."""
    with open(QUESTIONS_FILE, "w") as file:
        json.dump(questions, file, indent=4)

# Add a new question interactively
def add_question():
    """Interactively add a new question."""
    question = input("Enter the question: ")
    options = [
        input("Enter option A: "),
        input("Enter option B: "),
        input("Enter option C: "),
        input("Enter option D: ")
    ]
    correct_answer = input("Enter the correct answer (A-D): ").upper()
    
    # Validate the correct answer
    while correct_answer not in ["A", "B", "C", "D"]:
        print("Invalid answer! Please enter A, B, C, or D.")
        correct_answer = input("Enter the correct answer (A-D): ").upper()
    
    return {
        "question": question,
        "options": [f"A. {options[0]}", f"B. {options[1]}", f"C. {options[2]}", f"D. {options[3]}"],
        "correct_answer": correct_answer
    }

# Main function for the question adder application
def main():
    """Main function for the question adder application."""
    print("Welcome to the Quiz Question Adder!")
    print("This application allows you to add new questions to the quiz.\n")
    
    # Load existing questions
    questions = load_questions()
    
    while True:
        print("\n--- Menu ---")
        print("1. Add a new question")
        print("2. View all questions")
        print("3. Save and exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            # Add a new question
            new_question = add_question()
            questions.append(new_question)
            print("Question added!")
        elif choice == "2":
            # View all questions
            if not questions:
                print("No questions found.")
            else:
                print("\n--- Questions ---")
                for i, q in enumerate(questions, start=1):
                    print(f"{i}. {q['question']}")
                    for option in q["options"]:
                        print(option)
                    print(f"Correct Answer: {q['correct_answer']}\n")
        elif choice == "3":
            # Save questions and exit
            save_questions(questions)
            print("Questions saved. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the question adder application
if __name__ == "__main__":
    main()