from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')
your_name = "Mitch"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)