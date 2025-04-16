from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
your_name = "Mitch"

Users = {
    'Mitchel' : '1234',
    'Mitch' : '1234'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

#checks if username and password are correct from what I hard coded
        if username in Users and Users[username] == password:
            return redirect(url_for('success', username=username)) #redirect to success page
        else:
            return redirect(url_for('error'))
    
    return render_template('login.html')

@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)

@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)