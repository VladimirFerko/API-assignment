from ast import Delete
from re import X
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import jinja2
from forms import CreatePostForm, IdSubmitForm, ModifyForm, ModifyPostForm
import requests


# creating an instance of class Flask
app = Flask(__name__)

# configuration
app.config['SECRET_KEY'] = 'bedd54fa8a539ff68972ab70e36df261'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

# initialized the database
db = SQLAlchemy(app)

# creating a model (SQL table) with the columns
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(50), nullable = False)
    body = db.Column(db.String(200), nullable = False)

    # method for returning an existing elements
    def __repr__(self):
        return f'title - {self.title}'



# the first base page
@app.route('/')
def home():
    return render_template('index.html')


# app route for creating a post
@app.route('/create', methods = ['GET', 'POST'])
def create():
    # creating forms and waiting for user to submit
    form = CreatePostForm()
    if form.validate_on_submit():
        # getting data
        data = form.data
        user = requests.get('https://jsonplaceholder.typicode.com/posts', params = {"userId": f"{data['user_id']}"}).json()
        # checking if the user does exist
        if len(user) == 0:
            return render_template('create.html', form = form, data = "I am sorry, this user does not exist")
        else:
            # adding him into a database and redirecting to a home page
            new_post = Posts(userId = data['user_id'], title = data['title'], body = data['body'])
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('home'))


    try:
        return render_template('create.html', form = form, data = data)
    except UnboundLocalError:
        return render_template('create.html', form = form)
        


@app.route('/modify', methods = ['POST', 'GET'])
def modify():
    form = ModifyForm()
    
    # modify branch
    if form.validate_on_submit():
        id_post = form.data['id_post']
        try:
            update = Posts.query.filter_by(id = int(id_post)).first()
        except ValueError:
            return render_template('modify.html', form = form, print = 'Id can be only in numeric type')


        if not update:
            return render_template('modify.html', form = form, print = f"There is no post with id '{id_post}'")


        
        return redirect(url_for('modify_post', num = id_post))



    


    return render_template('modify.html', form = form)


@app.route('/modify/post/<int:num>', methods = ['POST', 'GET'])
def modify_post(num):
    db_post = Posts.query.filter_by(id = int(num)).first()
    form = ModifyPostForm()
    if form.validate_on_submit():  
        update = Posts.query.filter_by(id = int(num)).first()
        update.title = form.data['title']
        update.body = form.data['body']
        db.session.commit()

        return redirect(url_for('home'))



    return render_template('modify_post.html', title = db_post, form = form)



@app.route('/delete', methods = ['POST','GET'])
def delete():
    form = ModifyForm()
    id_post = form.data['id_post']


    # delete branch
    if form.validate_on_submit():
        # getting post informations from the database
        try:
            db_post = Posts.query.filter_by(id = int(id_post)).first()
        except ValueError:
            return render_template('modify.html', form = form, print = 'Id can be only in numeric type')
            
        if not db_post:
            return render_template('modify.html', form = form, print = f'I am sorry, element with id "{id_post}" does not exist')

        db.session.delete(db_post)
        db.session.commit()


        return render_template('index.html')


    return render_template('delete.html', form = form)

# route for selecting which one post do you want to see
@app.route('/show', methods = ['GET', 'POST'])
def show():
    # creating forms and waiting to submit
    form = IdSubmitForm()
    if form.validate_on_submit():
        # getting data
        num = form.data['id_post']
        posts = Posts.query.all()

        # checking if the users demand is in the database
        try:
            for item in posts:
                if int(item.id) == int(num):
                    # redirecting to show user his demand
                    return redirect(url_for('show_post', num = int(num)))
        except ValueError:
            # rendering web to tell user he is seeking for sth what is not existing the database
            return render_template('show.html', form = form, title = 'ID can be only a numeric value')

        # getting request from external API
        post = requests.get(f'https://jsonplaceholder.typicode.com/posts/{num}').json()

        # checking if the post is present in the database 
        if len(post) == 0:
            return render_template('show.html', form = form, title = f'I am sorry, there is no post with id "{num}"')

        # redirecting to show user his demand
        return redirect(url_for('show_post', num = int(num)))


    # first web page opening (asking for user input)
    return render_template('show.html', form = form)


@app.route('/show/posts/<int:num>')
def show_post(num):

    # checking database
    posts = Posts.query.all()
    for item in posts:
        if int(item.id) == int(num):
            return render_template('show_post.html', title = item.title, body = item.body)
   


    # case i dont have any post in my database API method
    post = requests.get(f'https://jsonplaceholder.typicode.com/posts/{num}').json()
    return render_template('show_post.html', title = post['title'], body = post['body'])





if __name__ == '__main__':
    app.run(debug = True)