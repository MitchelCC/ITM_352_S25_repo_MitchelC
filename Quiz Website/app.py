from flask import Flask, render_template,jsonify,request, redirect, url_for, session, flash
import json
import os
import random

app = Flask(__name__)
app.secret_key = '1234'


#file paths
Questions_file = 'questions.json'
users_file = 'users.json'
scores_file = 'scores.json'

#initiliaze empty files if they dont exist
if not os.path.exists(Questions_file) or os.path.getsize(Questions_file) == 0:
    with open(Questions_file, 'w') as f:
        json.dump([
            {
                "question": "Sample Question 1",
                "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
                "original_correct": 0
            }
        ], f)
    
def load_users():
    if not os.path.exists(users_file):
        return {}
    try:
        with open(users_file, 'r') as f:
            content = f.read()
            if not content.strip():
                return{}
            return json.loads(content)
    except json.JSONDecodeError:
        return{}

def save_users(users):
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Safely get form values with defaults
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        # Validate inputs first
        if not username or not password:
            flash('Username and password are required!')
            return redirect(url_for('login'))

        # Now safely load users
        users = load_users()

        # Auto-create user if new
        if username not in users:
            users[username] = {
                'password': password,
                'high_score': 0
            }
            save_users(users)
            flash(f"New user {username} created!")

        # Verify credentials
        if users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('quiz'))
        else:
            flash('Incorrect password')
            return redirect(url_for('login'))

    # Handle GET requests
    return render_template('login.html')

@app.route('/api/questions', methods=['GET'])
def get_questions():
    try:
        questions = load_questions()
        if not questions:
            return jsonify({'error': 'No questions'}), 404
        return jsonify(questions)
    except Exception as e:
        return jsonify({'Error': str(e)}), 500

@app.route('/api/scores', methods = ['POST'])
def submit_score():
    if 'username' not in session:
        return jsonify({'error': 'Unauthoried'}), 401
    
    data = request.get_json()
    if not data or 'score' not in data:
        return jsonify({'error': 'invalid data'}), 400
    
    try:
        with open(scores_file, 'a') as f:
            f.write(f"{session['username']}: {data['score']}\n")
        return jsonify ({'message': 'score saved'}), 200
    except Exception as e:
        return jsonify ({'error': str(e)}), 500

#loading my questions
def load_questions(): 
    try:
        if not os.path.exists(Questions_file):
            with open(Questions_file, 'w') as f:
                json.dump([], f)
            return []
        with open(Questions_file, 'r') as f:
            questions = json.load(f)
        
        if not isinstance(questions, list):
            raise ValueError("Invalid questions format")
        
        valid_questions = []
        for q in questions:
            if all(key in q for key in ['question', 'options', 'original_correct']):
                random.shuffle(q['options'])#randomizes pptions
                q['correct_answer'] = q['options'][q['original_correct']]
                valid_questions.append(q)
            
        random.shuffle(valid_questions)
        return valid_questions

    except Exception as e:
        print(f"Error loading questions: {str(e)}")
        return []

@app.route ('/quiz', methods = ['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    if 'questions' not in session:
        try:
            questions = load_questions()
            if not questions:
                flash("No questions.")
                return redirect(url_for('index'))
            session['questions'] = questions
            session['current_question'] = 0
            session['score'] = 0
            session['incorrect'] = []
        except Exception as e:
            flash ('Failed to load questions')
            return redirect(url_for('index'))

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        question = session['questions'][session['current_question']]
        
        if user_answer == question['correct_answer']:
            session['score'] += 1
        else: session['incorrect'].append({
            'question' : question['question'],
            'correct' : question['correct_answer'],
            'user_answer' : user_answer
        })

        session['current_question'] += 1
        if session['current_question'] >= len(session['questions']):
            return redirect(url_for('result'))
    
    question = session ['questions'][session['current_question']]
    return render_template('quiz.html', question = question, progress = f"{session['current_question'] + 1}/{len(session['questions'])}")

@app.route('/result')
def result():
    if 'username' not in session or 'score' not in session:
        return redirect(url_for('index'))
    try:
        with open(scores_file, 'a') as f:
            f.write(f"{session['username']}: {session['score']})\n")
    except Exception as e:
        flash("Couldn't save score. Please try again.")
    result = {
        'score': session['score'],
        'total': len(session['questions']),
        'incorrect': session['incorrect']
    }
    session.clear()
    return render_template('result.html', result = result)   
    
if __name__ == '__main__':
    app.run(debug=True)