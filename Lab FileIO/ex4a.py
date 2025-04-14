import json 
quiz_quest = {"What is the capital of France?": "Paris", "What is the capital of Germany?": "Berlin", "What is the capital of Italy?": "Rome", "What is the capital of Spain?": "Madrid", "What is the capital of Portugal?": "Lisbon"}

with open("quiz_quest.json", "w") as json_file:
    json.dump(quiz_quest, json_file, indent=4)
    