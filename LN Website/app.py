from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import flash

app = Flask(__name__)
app.secret_key = 'MitchelCC'  # Replace with a real secret key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Mock user database (password fixed as string)
users = {
    'admin': {
        'password': 'MitchelAC',  # Now a string instead of tuple
        'name': 'Admin'
    }
}

# Mock novels data
novels = {
    1: {
        "title": "Solo Leveling",
        "cover": "solo_leveling.jpg",
        "summary": "In a world where hunters battle monsters...",
        "chapters": 200
    }
}

# User class
class User(UserMixin):
    pass

# REQUIRED: User loader callback
@login_manager.user_loader
def load_user(user_id):
    if user_id not in users:
        return None
    user = User()
    user.id = user_id
    return user

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if user exists and password matches
        if username in users and users[username]['password'] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect(url_for('home'))
        
        flash('Invalid username or password')
        return redirect(url_for('login'))
    
    return render_template('login.html')  # Corrected template path

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html', novels=novels)

@app.route('/novel/<int:novel_id>')
@login_required
def novel(novel_id):
    return render_template('novel.html', novel=novels.get(novel_id))

if __name__ == '__main__':
    app.run(debug=True)