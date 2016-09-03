from __init__ import db

class Request(db.Model):
    __tablename__ = 'Request'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(1000))
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref=db.backref('requests', lazy='dynamic'))
    priority = db.Column(db.Integer)
    targetdate = db.Column(db.Date)
    ticketurl = db.Column(db.String(200))
    productarea_id = db.Column(db.Integer, db.ForeignKey('productarea.id'))
    productarea = db.relationship('ProductArea', backref=db.backref('requests', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))

    def __init__(self, title, description, client, priority, targetdate, ticketurl, productarea, user):
        self.title = title
        self.description = description
        self.client = client
        self.priority = priority
        self.targetdate = targetdate
        self.ticketurl = ticketurl
        self.productarea = productarea
        self.user = user

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
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    client = db.relationship('Client', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, email, password, idAdmin, client):
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = False
        self.client = client

    def __repr__(self):
        return '<User> %r' % self.username
