from flask import Flask, render_template, request

app = Flask(__name__)
your_name = "Mitch"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print (f"Username: {username}, Password: {password}")
        return "Form submitted!"
    
    return render_template('login.html')



    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)