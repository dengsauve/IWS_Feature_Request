from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_URI_DATABASE'] = "sqlite:////tmp/temp.db"
db = SQLAlchemy(app)

import .models

@app.route('/')
def render_main():
    return render_template('login.html')

@app.route('/home')
def render_home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
