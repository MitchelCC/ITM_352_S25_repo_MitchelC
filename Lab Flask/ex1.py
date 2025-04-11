from flask import flask

app = Flask(__name__)
your_name = "Mitch"

@app.route('/')
def get_welcome():
    return f"Welcome to {your_name}'s web site!"

if __name__ == '__main__':
    app.run(debug=True)