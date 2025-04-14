import json

with open ("quiz_quest.json", "r") as json_file:
    quiz_quest = json.load(json_file)

print("Quiz questions and answers: ")
for question, answer in quiz_quest.items():
    print(f"Q: {question}")
    print(f"A: {answer}\n")