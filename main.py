from flask import Flask, render_template, request, redirect, session
from replit import db
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.environ['sessionKey']

# Check if the database is initialized
if "posts" not in db:
    db["posts"] = []

# Hardcoded user credentials (for simplicity, in a real application, you would use a more secure method)
USERNAME = "marina"
PASSWORD = "marina"

# Add the custom filter to the Jinja environment
app.jinja_env.filters['timestamp_to_date'] = lambda timestamp: datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('blog.html', posts=db['posts'])
    else:
        return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

@app.route('/add_post', methods=['POST'])
def add_post():
    if 'logged_in' in session and session['logged_in']:
        header = request.form['header']
        text = request.form['text']

        # Automatically add the current date
        timestamp = datetime.timestamp(datetime.now())

        db['posts'].append({'header': header, 'timestamp': timestamp, 'text': text})
        return redirect('/')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
