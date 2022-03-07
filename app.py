from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creating an instance of class Flask
app = Flask(__name__)

# added database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# initialized the database
db = SQLAlchemy(app)

# creating a model (SQL table)
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, nullable = False, unique = True)
    title = db.Column(db.String(50), nullable = False)
    body = db.Column(db.String(200), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    # method for returning an existing models
    def __repr__(self):
        return f'title - {self.title}'



# the first base page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/modify')
def modify():
    return render_template('modify.html')

@app.route('/show')
def show():
    return render_template('show.html')



if __name__ == '__main__':
    app.run(debug = True)