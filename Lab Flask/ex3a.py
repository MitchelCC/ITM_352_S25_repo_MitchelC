from flask import Flask, render_template
import requests
app = Flask(__name__)

def get_meme(): 
    url = "https://meme-api.com/gimme/wholesomememes"
    response = requests.get("GET", url)

    if response.status_code == 200:
        data = response.json()
        return data['url'], data ['subreddit']
    else:
        return None, None
    
@app.route('/')
def index():
    meme_url, subreddit = get_meme()
    return render_template('memedex.html', meme_url=meme_url, subreddit=subreddit)

if __name__ == '__main__':
    app.run(debug=True)