import json
import os

#file paths to store and load data
QUESTIONS_FILE = "quiz_questions.json"
SCORES_FILE = "scores.json"
USERS_FILE = "users.json"

#load question from JSON file
def load_questions():
    """Load questions from the JSON file."""
    if not os.path.exists(QUESTIONS_FILE):
        return []  # Return an empty list if the file doesn't exist
    with open(QUESTIONS_FILE, "r") as file:
        return json.load(file)

#load users from JSON file
def load_users():
    """Load users from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return []  # Return an empty list if the file doesn't exist
    with open(USERS_FILE, "r") as file:
        return json.load(file)

#save users to json
def save_users(users):
    """Save users to the users.json file."""
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

# Register a new user
def register_user():
    """Register a new user."""
    username = input("Enter a username: ")
    users = load_users()
    if username in users:
        print("Username already exists. Please log in.")
        return None
    password = input("Enter a password: ")
    users[username] = {"password": password, "high_score": 0}
    save_users(users)
    print("Registration successful!")
    return username

#Log in an existing User
def login_user():
    """Log in an existing user."""
    username = input("Enter your username: ")
    users = load_users()
    if username not in users:
        print("Invalid username.")
        return None
    password = input("Enter your password: ")
    if users[username]["password"] != password:
        print("Invalid password.")
        return None
    print("Login successful!")
    return username

#save score to scores file
def save_score(username, score):
    """Save the user's score to the scores.txt file."""
    with open(SCORES_FILE, "a") as file:
        file.write(f"{username}: {score}\n")

#update high score of usr
def update_high_score(username, score):
    """Update the user's high score in the users.json file."""
    users = load_users()
    if score > users[username]["high_score"]:
        users[username]["high_score"] = score
        save_users(users)
        print(f"New high score for {username}: {score}!")

#Grand champ
def get_grand_champion():
    """Get the user with the highest score across all quizzes."""
    users = load_users()
    if not users:
        return None
    grand_champion = max(users.items(), key=lambda x: x[1]["high_score"])
    return grand_champion

# Ask a single question
def ask_question (question_data): 
    """Ask a single question and return whether the answer was correct."""
    print(f"\n{question_data['question']}")
    for option in question_data["options"]:
        print(option)   

    while True:
        answer = input("Enter your answer (A-D): ").upper()
        if answer in ["A", "B", "C", "D"]:
            break
        else:
            print("Invalid input! Please enter A, B, C, or D.")
    
    if answer == question_data["correct_answer"]:
        print("Correct!")
        return True
    else:
        print(f"Incorrect! The correct answer is {question_data['correct_answer']}.")
        return False

def run_quiz(username):
    """run the quiz application."""
    print(f"\nHello {username}, welcome to Quizy!")
    print("Let's get started!\n")

    #load questions
    questions = load_questions()
    if not questions:
        print("No questions found. Please add questions to start the quiz.")
        return
#initialize score
    score = 0 

#ask each question 
    for question in questions:
        if ask_question(question):
            score += 1

    print(f"\n{username}, your final score is: {score}/{len(questions)}")

    #save score and update high score 
    save_score(username, score)
    update_high_score(username, score)

    #display champ
    grand_champion = get_grand_champion()
    if grand_champion:
        print(f"\nGrand Champion: {grand_champion[0]} with a high score of {grand_champion[1]['high_score']}")

#main menu
def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\n--- Quizy Main Menu ---")
        print("1. Register")
        print("2. Log in")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            register_user()
        elif choice == "2":
            username = login_user()
            if username:
                run_quiz(username)
        elif choice == "3":
            print("Exiting Quizy. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()