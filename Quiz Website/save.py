from flask import Flask, render_template,jsonify, make_response, request, redirect, url_for, session, flash
import json
import os
import random
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = '1234'


#file paths
Questions_file = 'questions.json'
users_file = 'users.json'
scores_file = 'scores.json'
visitors_file = 'visitors.json'

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

def load_visitors():
    if not os.path.exists(visitors_file):
        return{}
    with open (visitors_file, 'r') as f:
        return json.load(f)
    
def save_visitors(visitors):
    with open (visitors_file, 'w') as f:
        json.dump(visitors, f, indent = 4)

@app.before_request
def track_users():
    if 'visitor_id' not in session:
        session['visitor_id'] = str(uuid.uuid4())
        session.permanent = True

    visitors = load_visitors()
    visitor_id = session ['visitor_id']

    if (visitor_id not in visitors and 
        request.endpoint not in ['welcome', 'static', 'login'] and 
        not request.path.startswith('/static')):
        return redirect(url_for('welcome'))

@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Please enter your name')
            return redirect(url_for('welcome'))
        
        visitors = load_visitors()
        visitors[session['visitor_id']] = {
            'name': name,
            'first_seen': datetime.now().isoformat(),
            'scores': []
        }
        save_visitors(visitors)
        return redirect(url_for('login'))
    
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('quizy_visitor', session['visitor_id'],
                        max_age = 60*60*24*31)
        
    return resp


@app.route('/history')
def history():
    visitors = load_visitors()
    visitor_data = visitors.get(session['visitor_id'], {})
    return render_template('history.html', user=visitor_data)

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
    visitors = load_visitors()
    visitor_id = session.get('visitor_id')
    
    if visitor_id in visitors:
        visitor_data = visitors[visitor_id]
        return render_template('index.html',
                             username=visitor_data['name'],
                             scores=visitor_data['scores'])
    
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
                original_correct_text = q['options'][q['original_correct']]
                random.shuffle(q['options'])#randomizes pptions
                q['correct_answer'] = original_correct_text
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
            session['start_time'] = datetime.now().isoformat()
            session['incorrect'] = []
        except Exception as e:
            flash ('Failed to load questions')
            return redirect(url_for('index'))

    current = session['current_question'] + 1
    total = len(session['questions'])
    progress_percent = int ((current/total) * 100)

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
        
        current = session['current_question'] + 1
        total = len (session['questions'])
        progress_percent = int((current/total) * 100)
    
    return render_template('quiz.html',
                           progress = f"{current}/{total}",question=session['questions'][session['current_question']],
                           progress_percent=progress_percent)
 
@app.route('/result')
def result():
    if 'username' not in session or 'score' not in session:
        return redirect(url_for('index'))
    
    start_time = datetime.fromisoformat(session['start_time'])
    time_taken = datetime.now() - start_time
    result = {
        'score': session['score'],
        'total': len(session['questions']),
        'time': str(time_taken).split('.')[0],
        'incorrect': session['incorrect'],
        'timestamp' : datetime.now().isoformat()

    }
    try: #saving to scores file
        with open(scores_file, 'a') as f:
            f.write(f"{session['username']}: {session['score']} ({time_taken})\n")
    except Exception as e:
        flash("Couldn't save score.")
   
     # Save to visitor history (new functionality)
    try:
        visitors = load_visitors()
        visitor_id = session.get('visitor_id')
        if visitor_id:
            # Create entry if it doesn't exist
            if visitor_id not in visitors:
                visitors[visitor_id] = {
                    'name': session.get('username', 'Anonymous'),
                    'scores': []
                }
            
            # Add new score
            visitors[visitor_id]['scores'].append({
                'score': result['score'],
                'total': result['total']
            })
            
            save_visitors(visitors)
            
    except Exception as e:
        flash("Couldn't save score. Please try again.")
        print(f"Error saving score: {str(e)}")
        
    # Clear only quiz-related session data (keep user info)
    quiz_keys = ['questions', 'current_question', 'score', 'incorrect', 'start_time']
    for key in quiz_keys:
        session.pop(key, None)

    return render_template('result.html', 
                    result=result,
                    username=session.get('username'))

if __name__ == '__main__':
    app.run(debug=True)