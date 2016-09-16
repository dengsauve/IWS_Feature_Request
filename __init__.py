#!/usr/bin/env python

from flask import Flask, render_template, request, url_for, redirect, session, escape
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////var/www/FlaskApp/FlaskApp/database/flaskapp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "WhatASuperSecretKeyIhavemade!$@%#^$&$*"

class Request(db.Model):
    __tablename__ = 'Request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(1000))
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client = db.relationship('Client', backref=db.backref('requests', lazy='dynamic'))
    priority = db.Column(db.Integer)
    targetdate = db.Column(db.Date)
    ticketurl = db.Column(db.String(200))
    productarea_id = db.Column(db.Integer, db.ForeignKey('ProductArea.id'))
    productarea = db.relationship('ProductArea', backref=db.backref('requests', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))

    def __init__(self, title, description, client_id, priority, targetdate, ticketurl, productarea_id, user_id):
        self.title = title
        self.description = description
        self.client_id = client_id
        self.priority = priority
        self.targetdate = targetdate
        self.ticketurl = ticketurl
        self.productarea_id = productarea_id
        self.user_id = user_id

    def __repr__(self):
        return '<Request> %r' % self.title


class Client(db.Model):
    __tablename__ = 'Client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Client> %r' % self.name


class ProductArea(db.Model):
    __tablename__ = 'ProductArea'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ProductArea> %r' % self.name


class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(16))
    isAdmin = db.Column(db.Boolean)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'))
    client = db.relationship('Client', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, password, isAdmin, client_id):
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = False
        self.client_id = client_id

    def __repr__(self):
        return '<User> %r' % self.username

@app.route('/add_user')
def add_user():
    clients = Client.query.all()
    return render_template('newuser.html', clients=clients)


@app.route('/admin')
def god_mode():
    requests = Request.query.all()
    clients = Client.query.all()
    areas = ProductArea.query.all()
    users = User.query.order_by(User.username)
    return render_template('admin.html', requests=requests, clients=clients, areas=areas, users=users)

@app.route('/commit_user', methods=['POST'])
def commit_user():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    client_id = request.form['client_id']
    newbie = User(username, email, password, False, client_id)
    db.session.add(newbie)
    db.session.commit()
    return redirect('/admin')

@app.route('/home', methods=['POST'])
def render_home():
    if 'username' in session:
        user_id = escape(session['username'])
    else:
        user_id = 0
    username = User.query.filter_by(id=int(user_id))
    clients = Client.query.with_entities(Client.name)
    areas = ProductArea.query.with_entities(ProductArea.name)
    return render_template('index.html', areas=areas, clients=clients, user_id=user_id, username=username[0])

@app.route('/')
@app.route('/login/', strict_slashes=False)
def render_main():
    return render_template('login.html')

@app.route('/new_request/', methods=['POST'], strict_slashes=False)
def commit_request():
    title = request.form['title']
    description = request.form['description']
    client_id = request.form['client_id']
    priority = request.form['priority']
    targetdate = request.form['targetdate']
    url = request.form['url']
    productarea = request.form['productarea']
    user = request.form['user']

@app.route('/request_details/', methods=['POST'], strict_slashes=False)
def render_request_details():
    request_id = request.form['request_id']
    request_data = Request.query.filter_by(id=request_id)
    return render_template('details.html', requests=request_data)

@app.route('/user_details/', methods=['POST'], strict_slashes=False)
def render_user_details():
    user_id = request.form['user_id']
    user_data = User.query.filter_by(id=user_id)
    return render_template('users.html', users=user_data)

@app.route('/verify/', methods=['POST'], strict_slashes=False)
def check_credentials():
    input_username = request.form['username']
    input_password = request.form['password']
    usernames = User.query.with_entities(User.username)
    unames = []
    for i in usernames:
        unames.append(i.username)
    if input_username in unames:
        candidate = User.query.filter_by(username=input_username) # NEED TO CLEANLY VERIFY USERNAME INPUT!!!
        if candidate[0].password == input_password:
            session['username'] = candidate[0].id
            return redirect(url_for('.render_home')), 307
        else:
            return redirect(url_for('.render_main')), 307
    else:
        return redirect(url_for('.render_main')), 307


@app.errorhandler(404)
def render_page_not_found(error_message):
    return render_template('404.html', error=error_message)

@app.errorhandler(500)
def render_page_not_found(error_message):
    return render_template('500.html', error=error_message)

@app.errorhandler(400)
def render_page_not_found(error_message):
    return render_template('400.html', error=error_message)


if __name__ == '__main__':
    app.run(debug=True)
